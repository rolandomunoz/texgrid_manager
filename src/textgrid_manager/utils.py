from pathlib import Path

import mytextgrid as mtg

def scan_library(source_dir):
    source_dir = Path(source_dir)

    list_ = []
    for path in source_dir.glob('*.TextGrid'):
        tg = mtg.read_from_file(path, encoding='utf-8')
        tg.path = path
        list_.append(tg)
    return list_
