import json
from pathlib import Path
import re


def get_values_under_index(index):
    result = []
    result.extend(index['paths'])
    if 'chs' in index:
        for ch_dict in index['chs'].values():
            result.extend(get_values_under_index(ch_dict))
    return result


def split_string(s):
    result = s.split()
    for x in result.copy():
        result.extend(x.split('-'))
    result = filter(lambda x: x, result)
    return set(result)


def find_files(search_pattern):
    with open('index.json') as f:
        index = json.load(f)

    split_pattern = split_string(search_pattern)
    result = []

    for path in index:
        path = Path(path['path'])

        pattern_matched = 0
        for path_part in split_string(str(path.name)):
            for pattern in split_pattern:
                if re.match(f'^{re.escape(pattern)}', path_part, re.IGNORECASE):
                    pattern_matched += 1
                elif re.match(f'\.{re.escape(pattern)}', path.suffix, re.IGNORECASE):
                    pattern_matched += 1
        if pattern_matched >= len(split_pattern):
            result.append(str(path))
    return result


if __name__ == '__main__':
    print(find_files(input('Search for: ')))