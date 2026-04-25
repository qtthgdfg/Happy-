
[app]
title = System Service
package.name = sysservice
package.domain = com.system.service
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,android
orientation = portrait
android.permissions = INTERNET,FOREGROUND_SERVICE,WAKE_LOCK,RECEIVE_BOOT_COMPLETED,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,READ_PHONE_STATE,ACCESS_COARSE_LOCATION,ACCESS_FINE_LOCATION,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 26
android.ndk = 23b
android.sdk = 31
android.gradle_dependencies = 
android.arch = arm64-v8a
android.allow_backup = True
android.presplash_color = #000000
android.logcat_filters = *:S
android.foreground_service_type = dataSync
android.entrypoint = myservice.py
p4a.branch = develop
service.name = SystemForegroundService
service.description = System service for background operations
android.broadcast_receiver = BootReceiver
android.boot_receiver = True
android.wakelock = True
android.exclude_dirs = tests,__pycache__
android.add_src = src
fullscreen = 0
log_level = 2
warn_on_root = 1

