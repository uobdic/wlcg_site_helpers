from snakebite.client import AutoConfigClient
fs = AutoConfigClient()


def ls(paths=['/'], recurse=False):
    if not isinstance(paths, list) and not isinstance(paths, tuple):
        paths = [paths]
    for p in fs.ls(paths, recurse):
        yield p['path'], p['length']
