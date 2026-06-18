[app]

# (str) Title of your application
title = TikPhoto - محرر الصور

# (str) Package name
package.name = tikphoto

# (str) Package domain (needed for android/ios packaging)
package.domain = org.tikphoto

# (source.dir) Source code where the main.py live
source.dir = .

# (list) Source includes patterns, let's you select which files / directories to include in the source android app.
source.include_exts = py,png,jpg,kv,atlas,ttf

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
version.regex = __version__ = ['"](.+?)['"]
version.filename = %(source.dir)s/main.py

# (list) Application requirements
requirements = python3,kivy,opencv,pillow,numpy

# (str) Supported orientation (landscape, sensorLandscape, portrait or sensorPortrait)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Icon of the application
icon.filename = assets/icon.png

# (str) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA,ACCESS_FINE_LOCATION

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 23b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android app theme, default is ok for Kivy-based app
android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
p4a.bootstrap = sdl2

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warnings (1 = warn) [DEPRECATED]
warn_on_root = 1
