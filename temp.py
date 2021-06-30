import timeit
import json
from pathlib import Path
import re


def find_files1(file_name, root_dir='/Users/safwan'):
    result = []
    root = Path(root_dir)

    for path in root.iterdir():
        if re.match(re.escape(file_name), path.name, flags=re.IGNORECASE):
            result.append(str(path.resolve()))
        if path.is_dir():
            try:
                result.extend(find_files1(file_name, root_dir=path))
            except PermissionError:
                pass
    return result


def get_values_under_index(index):
    result = []
    result.extend(index['paths'])
    if 'chs' in index:
        for ch_dict in index['chs'].values():
            result.extend(get_values_under_index(ch_dict))
    return result


def find_files(file_name):
    with open('index.json') as f:
        index = json.load(f)
    sub_index = index
    for i, ch in enumerate(file_name):
        if i == len(file_name) - 1:
            sub_index = sub_index[ch]
            break
        sub_index = sub_index[ch]['chs']
    return get_values_under_index(sub_index)


print(find_files('cypress'))
