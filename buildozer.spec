[app]
title = System Service
package.name = sysservice
package.domain = com.system.service
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,FOREGROUND_SERVICE,WAKE_LOCK,RECEIVE_BOOT_COMPLETED,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,READ_PHONE_STATE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 26
android.ndk = 23b
android.sdk = 31
android.gradle_dependencies = 
android.arch = arm64-v8a
android.allow_backup = False
android.presplash_color = #000000
android.logcat_filters = *:S
android.foreground_service_type = dataSync
android.entrypoint = myservice.py
android.wakelock = True
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
