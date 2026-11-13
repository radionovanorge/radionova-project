"""WSGI entry point, with bounded diagnostics for stalled Django startup."""
import faulthandler
import os
import sys
import time

started = time.monotonic()
print("STARTUP django_loading", file=sys.stderr, flush=True)
# Stack frames only: no environment values, request data or local variables.
faulthandler.enable()
faulthandler.dump_traceback_later(30, repeat=True)
try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "radionova.settings")
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()
except BaseException:
    print(f"STARTUP django_failed elapsed={time.monotonic() - started:.2f}s", file=sys.stderr, flush=True)
    raise
finally:
    faulthandler.cancel_dump_traceback_later()
print(f"STARTUP django_ready elapsed={time.monotonic() - started:.2f}s", file=sys.stderr, flush=True)
