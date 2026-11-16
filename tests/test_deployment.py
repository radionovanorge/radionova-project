import importlib.util
from pathlib import Path
import subprocess
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


if __name__ == '__main__':
    unittest.main()
