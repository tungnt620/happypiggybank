DEBUG = False

ALLOWED_HOSTS = ['45.76.146.131']


REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_LOCATION = "redis://{host}:{port}/{db}".format(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

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