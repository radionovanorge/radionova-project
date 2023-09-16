from .base import *

DEBUG = False


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", default="postgres"),
        "USER": os.environ.get("POSTGRES_USER", default="radionova"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", default="R@dionova123"),
        "HOST": os.environ.get("POSTGRES_HOST", default="radionova.postgres.database.azure.com"),
        "PORT": 5432,
    }
}


try:
    from .local import *
except ImportError:
    pass
