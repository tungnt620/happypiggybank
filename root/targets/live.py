DEBUG = False

ALLOWED_HOSTS = ['45.76.146.131']

# LOGGER
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s|%(levelname)s|%(process)d:%(thread)d|%(filename)s:%(lineno)d|%(module)s.%(funcName)s|%(message)s',
        },
        'short': {
            'format': '%(asctime)s|%(levelname)s|%(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'main.log',
            'formatter': 'standard'
        },
        'django': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['django'],
            'propagate': True,
        },
    },
}