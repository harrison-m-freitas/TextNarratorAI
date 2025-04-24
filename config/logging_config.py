import os
from dotenv import load_dotenv

load_dotenv(override=True)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": LOG_LEVEL,
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "detailed",
            "level": LOG_LEVEL,
            "filename": os.path.join("logs", "app.log"),
            "when": "midnight",
            "backupCount": 7,
            "encoding": "utf-8",
        },
    },

    "root": {
        "handlers": ["console", "file"],
        "level": LOG_LEVEL,
    },

    "loggers": {
        # Silencia warnings de bibliotecas ruidosas
        "urllib3": {"level": "WARNING", "propagate": False},
        "asyncio": {"level": "WARNING", "propagate": False},
    },
}