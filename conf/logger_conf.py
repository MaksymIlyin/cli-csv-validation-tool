
def get_logging_config(log_filename):
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)8s] %(name)15s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        "filters": {
            "warnings_and_below": {
                "()" : "__main__.filter_maker",
                "level": "WARNING"
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
                "filters": ["warnings_and_below"]
            },
            "stderr": {
                "class": "logging.StreamHandler",
                "level": "ERROR",
                "formatter": "standard",
                "stream": "ext://sys.stderr"
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "standard",
                "filename": f"./logs/{log_filename}",
                "mode": "w"
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": [
                "stderr",
                "stdout",
                "file"
            ]
        }
    }
    return config
