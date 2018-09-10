import pandas as pd
import numpy as np
from plumbum import local
from pandas.compat import StringIO

davix_ls_recursive = local["davix-ls"]['-P', 'grid']['-l']['-r', 8]
davix_ls = local["davix-ls"]['-P', 'grid']['-l']


def ls(path, recursive=False):
    paths = davix_ls_recursive(path) if recursive else davix_ls(path)
    paths = [p for p in paths.split('\n') if 'Error:' not in p]
    paths = '\n'.join(paths)
    column_names = ['perm', '0', 'size', 'date', 'time', 'path']
    df = pd.read_csv(StringIO(paths), delim_whitespace=True, names=column_names)
    # folders should not contribute to size
    df['size'] = np.where(df['perm'].str.startswith('d'), 0, df['size'])
    df['ftype'] = np.where(df['perm'].str.startswith('d'), 'd', 'f')
    df['size'] = df['size'].astype(int)
    df['date'] = pd.to_datetime(df['date'])
    # davix chops off first /
    incomplete_path = ~df['path'].str.startswith('/')
    df['path'][incomplete_path] = '/' + df['path'][incomplete_path].astype(str)
    df.drop(['perm', '0', 'time'], inplace=True, axis=1)
    df = df[df.path != '/failed:']
    df['size'] = df['size'].astype(int)
    return df
