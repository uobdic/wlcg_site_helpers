'''
WARNING, this module is slow for recursive tasks, use davix instead.

GFAL2 tools support

    'DirectoryType', 'Dirent', 'FileType', 'GfaltEvent', 'Stat',
    'TransferParameters', '__class__', '__delattr__', '__dict__', '__doc__',
    '__format__', '__getattribute__', '__hash__', '__init__',
    '__instance_size__', '__module__', '__new__', '__reduce__',
    '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
    '__subclasshook__', '__weakref__',
    'abort_bring_online', 'access',
    'add_client_info', 'bring_online', 'bring_online_poll', 'cancel',
    'checksum', 'chmod', 'clear_client_info', 'directory',
    'event_side', 'file', 'filecopy', 'get_client_info', 'get_opt_boolean',
    'get_opt_integer', 'get_opt_string', 'get_opt_string_list',
    'get_plugin_names', 'get_user_agent', 'getxattr', 'gfalt_event',
    'listdir', 'listxattr', 'load_opts_from_file', 'lstat', 'mkdir',
    'mkdir_rec', 'open', 'opendir', 'readlink', 'release',
    'remove_client_info', 'rename', 'rmdir', 'set_opt_boolean',
    'set_opt_integer', 'set_opt_string', 'set_opt_string_list',
    'set_user_agent', 'setxattr', 'stat', 'symlink', 'transfer_parameters',
    'unlink'

Result of stat
    ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__',
    '__hash__', '__init__', '__instance_size__', '__module__', '__new__', '__reduce__',
    '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
    '__weakref__', 'st_atime', 'st_ctime', 'st_dev', 'st_gid', 'st_ino', 'st_mode', 'st_mtime',
    'st_nlink', 'st_size', 'st_uid']
'''

import gfal2
import os

fs = gfal2.creat_context()


def _ls(path):
    try:
        paths = fs.listdir(path)
        return [os.path.join(path, p) for p in paths]
    except:  # p not a directory
        return None


def _size(path):
    try:
        return fs.stat(path).st_size
    except:
        return None


def ls(paths=['/'], recurse=False):
    if not isinstance(paths, list) and not isinstance(paths, tuple):
        paths = [paths]
    for p in paths:
        items = _ls(p)
        if items is None:
            continue
        sizes = [_size(i) for i in items]

        for i, s in zip(items, sizes):
            yield i, s

        if recurse:
            subitems = ls(items, True)
            for j in subitems:
                yield j


def size(paths=['/']):
    if not isinstance(paths, list) and not isinstance(paths, tuple):
        paths = [paths]
    for p in paths:
        s = _size(p)
        if s is None:
            continue
        yield s
