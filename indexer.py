from pathlib import Path
import json
EXCLUDED_DIRS = ['Library', 'opt', 'node_modules']
EXCLUDED_EXTS = ['.plist']


def indexer(dir='/Users/safwan', index=None):
    if index is None:
        index = {}
    for path in filter(path_black_list_conditions, Path(dir).iterdir()):
        try:
            path.iterdir()
            index = indexer(path, index)
        except (PermissionError, NotADirectoryError):
            pass
        path_name = path.name
        index.setdefault(path_name[0], {'paths': [], 'chs': {}})
        sub_index = index
        for i, ch in enumerate(path_name):
            sub_index.setdefault(ch, {'paths': [], 'chs': {}})
            if i == len(path_name) - 1:
                sub_index[ch]['paths'].append(str(path.resolve()))
                break
            sub_index = sub_index[ch]['chs']
    print(f'{dir} done.')
    return index


def path_black_list_conditions(file):
    return not (
        file.name.startswith('.') or
        any(file.match(d) for d in EXCLUDED_DIRS) or
        any(file.name.endswith(ext) for ext in EXCLUDED_EXTS))


index = indexer()
with open('index.json', 'w') as f:
    json.dump(index, f)
