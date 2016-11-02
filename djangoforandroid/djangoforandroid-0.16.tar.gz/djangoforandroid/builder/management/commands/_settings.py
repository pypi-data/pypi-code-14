import os

ANDROID = {

    'APK': {
        #'name': "D4A",
        #'version': '0.1',
        #'package': 'com.yeisoncardona.d4a.testapk',
        #'icon': os.path.join(STATIC_ROOT, 'images', 'icon.png'),
        'statusbarcolor': '#7c962b',
        'orientation': 'portrait',
        'intent_filters': None,
        'download_name': "download",

    },

    #'KEY': {
        #'RELEASE_KEYSTORE': os.path.join(BASE_DIR, 'd4a.keystore'),
        #'RELEASE_KEYALIAS': 'd4a',
        #'RELEASE_KEYSTORE_PASSWD': 'MySuperSecurePassw',
        #'RELEASE_KEYALIAS_PASSWD': 'MySuperSecurePassw',
    #},

    'SPLASH': {
        'static_html': False,
        'resources': [],
    },

    'PORT': '8888',

    'PERMISSIONS': [],
    #'__PERMISSIONS': [],

    'BUILD': {
        'build': os.path.expanduser('~/.django-for-android'),
        'recipes': None,  #string
        'whitelist': None,
        'requirements': [],
        '__requirements': ['python3crystax', 'django', 'sqlite3', 'djangoforandroid'],
        'exclude_dirs': [],
        'include_exts': [],
        },

}

