import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
VAR_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "var"))


DEBUG = False
ALLOWED_HOSTS = ['project_oj.example.com']

ADMINS = (
    ('Admin', 'admin@mail.com'),
)

SERVER_EMAIL = "web@project_oj.example.com"


# ------------------------------ Databases ------------------------------------


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'project_oj',
        'USER': '',  # in secrets.json
        'PASSWORD': '',  # in secrets.json
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'project_oj',
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': '',
#        #'PORT': '',
#        'OPTIONS': {
#            'init_command': 'SET storage_engine=INNODB',
#        }
#    }
#}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(VAR_ROOT, "logfile.log"),
            'maxBytes': 1048576,
            'backupCount': 7,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
