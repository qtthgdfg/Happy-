[app]
title = System Service
package.name = sysservice
package.domain = com.system.service
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,android,openssl,libffi,requests,urllib3,chardet,idna,certifi
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,FOREGROUND_SERVICE,WAKE_LOCK,RECEIVE_BOOT_COMPLETED,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,READ_PHONE_STATE,READ_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.ndk = 25b
android.sdk = 30.0.3
android.gradle_dependencies = 
android.arch = arm64-v8a,armeabi-v7a
android.allow_backup = False
android.presplash_color = #000000
android.logcat_filters = *:S
android.foreground_service_type = dataSync
android.entrypoint = main.py
android.service = myservice:main.py
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
