import faulthandler, os, sys, time
faulthandler.enable()
faulthandler.dump_traceback_later(30, repeat=True)
print("DIAGNOSTIC: before migrations", flush=True)
os.environ["DJANGO_SETTINGS_MODULE"] = "radionova.test_settings"
from django.core.management import execute_from_command_line
execute_from_command_line(["manage.py", "migrate", "--noinput"])
faulthandler.cancel_dump_traceback_later()
print("DIAGNOSTIC: migrations complete", flush=True)
os.execvp("gunicorn", ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "--capture-output", "radionova.diagnostic_wsgi:application"])
