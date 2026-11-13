import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('packaging_script', ROOT / 'scripts/build_deploy_package.py')
packaging = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packaging)


class PackageTests(unittest.TestCase):
    def test_archive_contains_app_assets_but_no_environments_or_secrets(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(['git', 'init', '-q', folder], check=True)
            wanted = ['manage.py', 'requirements.txt', 'radionova/settings.py',
                      'radionova/wsgi.py', 'tears/migrations/0074_example.py',
                      'theme/static/css/dist/styles.css', 'static/admin/app.js']
            unwanted = ['venv/bin/python', '.venv312/bin/python', '.vscode/settings.json',
                        '.env', 'radionova/site.env', 'radionova/.env.production',
                        'radionova/local_settings.py', 'theme/node_modules/module/index.js',
                        'tears/__pycache__/models.pyc', 'static/release.zip', 'release.zip']
            for name in wanted + unwanted:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('fixture')
            subprocess.run(['git', 'add', '.'], cwd=root, check=True)
            (root / 'radionova/untracked_secret.py').write_text('must not ship')
            output = root / 'package.zip'
            packaging.build_package(root, output)
            with ZipFile(output) as archive:
                self.assertEqual(set(archive.namelist()), set(wanted))
                self.assertIsNone(archive.testzip())

    def test_missing_required_file_stops_packaging(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(['git', 'init', '-q', folder], check=True)
            with self.assertRaisesRegex(ValueError, 'Missing required tracked file'):
                packaging.build_package(root, root / 'package.zip')


class StartupTests(unittest.TestCase):
    def run_wsgi(self, setup):
        # Fake Django isolates the logging/timer contract from settings and databases.
        code = '''import faulthandler, runpy, sys, time, types
real_timer = faulthandler.dump_traceback_later
faulthandler.dump_traceback_later = lambda delay, **kw: real_timer(.15, **kw)
module = types.ModuleType('django.core.wsgi')
''' + setup + '''
module.get_wsgi_application = get_application
sys.modules['django'] = types.ModuleType('django')
sys.modules['django.core'] = types.ModuleType('django.core')
sys.modules['django.core.wsgi'] = module
try:
    runpy.run_path(sys.argv[1])
except RuntimeError:
    pass
time.sleep(.25)
'''
        return subprocess.run([sys.executable, '-c', code, str(ROOT / 'radionova/wsgi.py')],
                              capture_output=True, text=True, timeout=5).stderr

    def test_success_logs_duration_and_cancels_timer(self):
        output = self.run_wsgi('def get_application(): return object()')
        self.assertIn('STARTUP django_ready elapsed=', output)
        self.assertNotIn('Timeout', output)

    def test_failure_logs_failure_and_cancels_timer(self):
        output = self.run_wsgi('def get_application(): raise RuntimeError("fixture")')
        self.assertIn('STARTUP django_failed elapsed=', output)
        self.assertNotIn('django_ready', output)
        self.assertNotIn('Timeout', output)

    def test_stalled_startup_dumps_stack(self):
        output = self.run_wsgi('def get_application(): time.sleep(.35); return object()')
        self.assertIn('Timeout', output)
        self.assertIn('get_application', output)
        self.assertIn('STARTUP django_ready elapsed=', output)


if __name__ == '__main__':
    unittest.main()
