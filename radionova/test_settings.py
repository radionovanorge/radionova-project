from .settings import *
# Isolated test: no production database, storage or credentials.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "/home/radionova-test.sqlite3"}}
SECRET_KEY = "isolated-diagnostic-test-no-production-data"
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1", os.environ.get("WEBSITE_HOSTNAME", "test.invalid")]
USE_AZURE_STORAGE = False
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
MEDIA_ROOT = "/home/radionova-test-media"
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
WAGTAIL_USAGE_URL_PREFIX = MEDIA_URL
