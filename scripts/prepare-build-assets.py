"""Clear inherited Windows read-only flags before Quarto copies resources."""
import os
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    if os.name != 'nt':
        return
    count = 0
    # Only project resources and disposable build output; never touch vault originals.
    for folder in (ROOT / 'assets', ROOT / '_site'):
        if not folder.exists():
            continue
        for path in folder.rglob('*'):
            if path.is_symlink() or not path.is_file():
                continue
            if not path.resolve().is_relative_to(ROOT):
                continue
            mode = path.stat().st_mode
            if not mode & stat.S_IWRITE:
                try:
                    path.chmod(mode | stat.S_IWRITE)
                except OSError as error:
                    raise RuntimeError(f'Cannot make build resource writable: {path}. {error}') from error
                count += 1
    if count:
        print(f'Prepared {count} read-only build resources for Quarto.')


if __name__ == '__main__':
    main()
