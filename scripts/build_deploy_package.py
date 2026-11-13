"""Create the source ZIP consumed by Azure/Oryx, without local environments."""
import argparse
from pathlib import Path
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

APP_ROOTS = {"radionova", "tears", "theme", "static"}
APP_FILES = {"manage.py", "requirements.txt"}
EXCLUDED_DIRS = {"node_modules", "__pycache__", ".git", ".vscode", "venv", "env", "antenv"}


def include_path(path):
    parts = Path(path).parts
    return (
        bool(parts)
        and (parts[0] in APP_ROOTS or path in APP_FILES)
        and not any(p in EXCLUDED_DIRS or p.startswith(".venv") for p in parts)
        and not any(p.startswith(".env") or p.endswith(".env") for p in parts)
        and Path(path).name != "local_settings.py"
        and Path(path).suffix not in {".pyc", ".pyo", ".zip", ".sqlite3"}
    )


def build_package(root, destination):
    tracked = subprocess.check_output(
        ["git", "ls-files", "--cached", "-z"], cwd=root
    ).decode().split("\0")
    paths = sorted(p for p in tracked if include_path(p))
    for required in APP_FILES | {"radionova/settings.py", "radionova/wsgi.py"}:
        if required not in paths:
            raise ValueError(f"Missing required tracked file: {required}")
    with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
        for name in paths:
            source = root / name
            if source.is_symlink() or not source.is_file():
                raise ValueError(f"Expected a regular application file: {name}")
            archive.write(source, name)
    return len(paths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    count = build_package(root, args.destination)
    print(f"Packaged {count} files into {args.destination} ({args.destination.stat().st_size} bytes)")
