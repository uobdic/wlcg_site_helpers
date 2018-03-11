"""
    Provides functionality for bulk-deleting files on a storage element
"""
from __future__ import absolute_import, print_function
import gfal2
import os
import logging
import hdfs
import grid
import json


def get_folders(prefix, fs = hdfs, cache='localfs.json'):
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
    hdfs_but_not_grid = list(set_hdfs - set_grid)
    print('N items on HDFS but not on grid', len(hdfs_but_not_grid), '\n', '\n'.join(hdfs_but_not_grid[:5]))
    with open('hdfs_but_not_grid.json', 'w') as f:
        json.dump(hdfs_but_not_grid, f)

    grid_but_not_hdfs = list(set_grid - set_hdfs)
    print('N items on grid but not on hdfs', len(grid_but_not_hdfs), '\n', '\n'.join(grid_but_not_hdfs[:5]))
    with open('grid_but_not_hdfs.json', 'w') as f:
        json.dump(grid_but_not_hdfs, f)
