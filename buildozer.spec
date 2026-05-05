# buildozer.spec - Complete configuration for background service APK

[app]

# (str) Title of your application
title = System Service

# (str) Package name
package.name = systemservice

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.0,pyjnius,android,plyer

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
# This is CRITICAL for background service execution!
services = Service:service.py

# (str) Service entry point file
service.source = %(source.dir)s/service.py

# (list) List of permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,\
    FOREGROUND_SERVICE,FOREGROUND_SERVICE_DATA_SYNC,FOREGROUND_SERVICE_SPECIAL_USE,\
    WAKE_LOCK,RECEIVE_BOOT_COMPLETED,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,\
    POWER_SAVE_MODE_CHANGED,ACCESS_BACKGROUND_SERVICE,\
    READ_PHONE_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (list) features of the app
android.features = android.hardware.wifi

# (list) Targeted Android SDK version
android.api = 33

# (str) Minimum Android SDK version
android.minapi = 21

# (int) Target NDK version
android.ndk = 25b

# (str) Gradle version
android.gradle_dependencies = 'androidx.core:core:1.10.1'

# (list) Java classes to add as activities
# android.add_activities = 

# (list) Java classes to add as services
# android.add_services = 

# (list) Android library projects to add
# android.add_libs_armeabi_v7a = 
# android.add_libs_arm64_v8a = 
# android.add_libs_x86 = 
# android.add_libs_x86_64 = 

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi_v8a

# (int) overrides automatic versionCode computation (used in build.gradle)
# android.numeric_version = 1

# (str) Bootstrap type (service_library, sdl2_gradle or webview)


# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (bool) Copy library instead of making libpymodules.so
# android.copy_libs = 1

# (str) The Android app bundle architecture
# android.app_bundle_arch = arm64-v8a, armeabi-v7a

# ----------------------------------------------------------
# Android SERVICE configuration
# ----------------------------------------------------------

# (str) Foreground service notification channel name
android.notification_channel_name = System Service

# (str) Foreground service notification title
android.notification_title = Running Background Service

# (str) Foreground service notification text
android.notification_text = Service is running in background

# (str) Foreground service notification icon
# android.notification_icon = 

# (str) Foreground service notification importance (min, low, default, high, max)
android.notification_importance = low

# (str) Foreground service type
android.foreground_service_type = dataSync

# (str) Service bootstrap - use 'service_library' for PythonService
# This MUST be set for services to work properly
p4a.bootstrap = sdl2_gradle

# ----------------------------------------------------------
# Build configuration
# ----------------------------------------------------------

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# android.permissions already defined above

# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------

# (str) Log level (trace, debug, info, warning, error, critical)
log_level = 2

# (bool) Enable logcat output
android.logcat = 1

# Advanced: specify which recipes to use
# osx.kivy_version = 1.11.1

# Extend buildozer hooks
# p4a.hook = /path/to/hook.py

# Extend source configurations for android
# p4a.source_dir = /path/to/python-for-android

# (bool) Skip Android SDK/NDK update check
# android.skip_update = False

# (bool) Create an archive (.apk) release
android.release_artifact = apk

# (str) Keystore path for release
# android.release.keystore = /path/to/keystore

# (str) Keystore alias
# android.release.keyalias = keyalias

# (str) Keystore password
# android.release.keystore_password = password

# (str) Key password
# android.release.key_password = password

# [buildozer]
