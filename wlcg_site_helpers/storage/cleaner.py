"""
    Provides functionality for bulk-deleting files on a storage element
"""

import gfal2
import os
import logging
from snakebite.client import AutoConfigClient

dtx_dir = [
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
    'unlink']

ctx = gfal2.creat_context()
hdfs = AutoConfigClient()


def delete_subfolders(parentDir, exclude=[], retainStructureLevel=0, noop=False):
    """

    """
    subfolders = expand_subfolders(parentDir, exclude, retainStructureLevel)
    for s in subfolders:
        try:
            logging.info('Deleting {0}'.format(s))
            if not noop:
                ctx.rmdir(s)
        except Exception, e:
            logging.error('Got error {0}'.format(e))
    # add check for HDFS remains


def expand_subfolders(parentDir, exclude, level,):
    try:
        subfolders = ctx.listdir(parentDir)
    except Exception, e:
        logging.error('Got error {0}'.format(e))
        return []
    subfolders = [
        os.path.join(parentDir, s) for s in subfolders if s not in exclude
    ]
    for l in range(level):
        subdirs = []
        for s in subfolders:
            try:
                dirs = ctx.listdir(s)
                subdirs.extend([os.path.join(s, d) for d in dirs])
            except Exception, e:
                logging.error('Got error {0}'.format(e))
        subfolders = subdirs
    return subfolders


def delete_hdfs_dir(directory):
    tokens = directory.split('/')
    hdfs_path = os.path.join(*tokens[3:])
    hdfs.rmdir(hdfs_path)


if __name__ == '__main__':
    base = 'davs://lcgse01.phy.bris.ac.uk/dpm/phy.bris.ac.uk/home/cms/store/PhEDEx_LoadTest07/'
    exclude = [
        'LoadTest07_Bristol',
        'LoadTest07_Debug_T2_UK_SGrid_Bristol'
    ]
    retainStructureLevel = 2
    delete_subfolders(base, exclude, retainStructureLevel, False)
