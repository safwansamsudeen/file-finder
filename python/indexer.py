from pathlib import Path
import json

DIRS = ['/Applications', '/Users/safwan']
EXCLUDED_PATHS = ['Library', 'opt', 'node_modules', '__pycache__', 'Icon?']
EXCLUDED_EXTS = ['.plist']


def path_black_list_conditions(file):
    return not (
        file.name.startswith('.') or
        any(file.match(d) for d in EXCLUDED_PATHS) or
        any(file.suffix == ext for ext in EXCLUDED_EXTS))


def indexer(dirs, index=None):
    if index is None:
        index = []

    for dir in dirs:
        for path in sorted(filter(path_black_list_conditions, Path(dir).iterdir())):
            if is_folder(path):
                indexer([path], index)

            index.append({
                'path': str(path.resolve()),
            })
        print(f'{dir} done.')
    return index


def is_folder(path):
    if path.suffix == '.app':
        return False
    try:
        list(path.iterdir())
    except (PermissionError, NotADirectoryError):
        return False
    return True


index = indexer(DIRS)
with open('index.json', 'w') as f:
    json.dump(index, f)
