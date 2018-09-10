"""
    Provides functionality for bulk-deleting files on a storage element
"""
from __future__ import absolute_import, print_function
import os
import hdfs
import grid
import json


def get_folders(prefix, fs=hdfs, cache='localfs.json'):
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f)
    folders = list(remove_prefix(fs.ls(prefix, True), prefix))
    with open(cache, 'w') as f:
        json.dump(folders, f)
    return folders


def remove_prefix(paths, prefix):
    for p in paths:
        yield p.replace(prefix, '')


if __name__ == '__main__':
    prefix_grid = 'davs://lcgse01.phy.bris.ac.uk/dpm/phy.bris.ac.uk/home/cms/store'
    prefix_localfs = '/dpm/phy.bris.ac.uk/home/cms/store'

    folders_hdfs = get_folders(prefix_localfs, fs=hdfs, cache='localfs.json')
    folders_grid = get_folders(prefix_grid, fs=grid, cache='grid.json')

    set_hdfs = set(folders_hdfs)
    set_grid = set(folders_grid)
    tmp_paths = []
    for path in set_grid:
        if path.startswith('/temp'):
            tmp_paths.append('/temp')

    with open('temp.json', 'w') as f:
        json.dump(tmp_paths, f)
