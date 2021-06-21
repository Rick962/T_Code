import os

_logfile_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)), r'logs',
                             r'log.log')

logconfig = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(filename)s %(funcName)s %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 当达到50MB时分割日志
            'maxBytes': 1024 * 1024 * 50,
            # 最多保留50份文件
            'backupCount': 50,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': False,
            'filename': _logfile_path,
            'formatter': 'verbose',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],  # 环境部署，'handlers': ['file', 'console'] ->'handlers': ['file']
            'level': 'DEBUG',
        },
    }
}
