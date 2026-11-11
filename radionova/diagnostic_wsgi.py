import faulthandler
import os
import sys
import time
faulthandler.enable()
faulthandler.dump_traceback_later(30, repeat=True)
started = time.monotonic()
print("DIAGNOSTIC: loading Django for commit 5cf3d63", file=sys.stderr, flush=True)
os.environ["DJANGO_SETTINGS_MODULE"] = "radionova.test_settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
faulthandler.cancel_dump_traceback_later()
print(f"DIAGNOSTIC: Django ready after {time.monotonic()-started:.2f}s", file=sys.stderr, flush=True)
