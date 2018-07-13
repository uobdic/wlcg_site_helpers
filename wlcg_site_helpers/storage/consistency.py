"""
    Provides functionality for bulk-deleting files on a storage element
"""
from __future__ import absolute_import, print_function
import gfal2
import os
import logging
import json
from .backend import hdfs
from .backend import davix
import pandas as pd

logger = logging.getLogger(__name__)

def get_folders(prefix, ls_func = hdfs.ls, cache='localfs.csv'):
    if os.path.exists(cache):
        logger.info('Found cache file {0} ... loading data'.format(cache))
        with open(cache) as f:
            return pd.read_csv(f, index_col=0)

    logger.info('Writing results to cache ({0})'.format(cache))
    df = ls_func(prefix, True)
    df.to_csv(cache)
    return df

def get_cache_files(cache_path):
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    
    cache_files = ['local_entries.csv', 'grid_entries.csv', 'local_but_not_grid.csv', 'grid_but_not_local.csv']
    return [os.path.join(cache_path, f) for f in cache_files]

def local_entries(local_path, ls_func, cache_path='/tmp'):
    cache_local_entries, _, _, _ = get_cache_files(cache_path)
    entries_local = get_folders(local_path, ls_func, cache_local_entries)
    return entries_local

def grid_entries(grid_path, ls_func, cache_path='/tmp'):
    _, cache_grid_entries, _, _ = get_cache_files(cache_path)
    entries_grid = get_folders(grid_path, ls_func, cache_grid_entries)
    return entries_grid

def get_diff(df1, df2, cache='diff.csv'):
    if os.path.exists(cache):
        logger.info('Found cache file {0} ... loading data'.format(cache))
        with open(cache) as f:
            return pd.read_csv(f, index_col=0)

    df = pd.merge(df1, df2, how='outer', indicator=True, on='path')
    df1_only = df[df._merge == 'left_only']
    df1_only = df1_only.rename(columns={'size_x':'size', 'date_x':'date', 'ftype_x':'ftype'})
    df1_only = df1_only.drop(['size_y', 'date_y', 'ftype_y', '_merge'], axis=1)
    logger.info('Writing results to cache ({0})'.format(cache))
    df1_only.to_csv(cache)

    return df1_only

def diff_local_but_not_grid(entries_grid, entries_local, cache_path='/tmp'):
    _, _, cache_diff_local_grid, _ = get_cache_files(cache_path)
    local_but_not_grid = get_diff(entries_local, entries_grid, cache_diff_local_grid)
    msg = '{0} items on local FS but not on grid'.format(len(local_but_not_grid))
    logger.info(msg)
    return local_but_not_grid

def diff_grid_but_not_local(entries_grid, entries_local, cache_path='/tmp'):
    _, _, _, cache_diff_grid_local = get_cache_files(cache_path)
    grid_but_not_local = get_diff(entries_grid, entries_local, cache_diff_grid_local)
    msg = '{0} items on grid but not on local FS'.format(len(grid_but_not_local))
    logger.info(msg)
    return grid_but_not_local

def check(grid_path, local_path, localfs=hdfs, cache_path='/tmp'):
    entries_local = local_entries(local_path, localfs.ls, cache_path)
    entries_grid = grid_entries(grid_path, grid.ls, cache_path)

    local_but_not_grid = diff_local_but_not_grid(entries_grid, entries_local, cache_path)
    
    grid_but_not_local = diff_grid_but_not_local(entries_grid, entries_local, cache_path)
    return grid_but_not_local, local_but_not_grid
