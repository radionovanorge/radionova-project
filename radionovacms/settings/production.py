from .base import *

DEBUG = False
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z#8!v)s!2ehk@ik_!p2h*u#cl!sa#-g5n65pzby+#mt1%ttt87"

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
