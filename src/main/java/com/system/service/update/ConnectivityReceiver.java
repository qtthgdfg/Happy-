// ConnectivityReceiver.java
package com.system.service.update;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Build;

public class ConnectivityReceiver extends BroadcastReceiver {
    
    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent.getAction();
        
        if (action == null) {
            return;
        }
        
        switch (action) {
            case ConnectivityManager.CONNECTIVITY_ACTION:
            case "android.net.wifi.WIFI_STATE_CHANGED":
            case "android.net.wifi.STATE_CHANGE":
                handleConnectivityChange(context);
                break;
        }
    }
    
    private void handleConnectivityChange(Context context) {
        try {
            ConnectivityManager cm = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
            if (cm == null) return;
            
            NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
            boolean isConnected = activeNetwork != null && activeNetwork.isConnected();
            
            if (isConnected) {
                // Network available - notify service
                notifyService(context, "network_available");
                
                // Check if service is running
                checkAndStartService(context);
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void notifyService(Context context, String action) {
        try {
            Intent serviceIntent = new Intent(context, SystemService.class);
            serviceIntent.setAction(action);
            
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(serviceIntent);
            } else {
                context.startService(serviceIntent);
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
    
    private void checkAndStartService(Context context) {
        try {
            ActivityManager manager = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
            if (manager != null) {
                boolean running = false;
                
                for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
                    if (service.service.getClassName().contains(context.getPackageName())) {
                        running = true;
                        break;
                    }
                }
                
                if (!running) {
                    Intent serviceIntent = new Intent(context, SystemService.class);
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                        context.startForegroundService(serviceIntent);
                    } else {
                        context.startService(serviceIntent);
                    }
                }
            }
        } catch (Exception e) {
            // Silent fail
        }
    }
}
