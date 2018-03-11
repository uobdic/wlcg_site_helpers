import gfal2
import os



fs = gfal2.creat_context()

def ls(paths = ['/'], recurse=False):
    if not isinstance(paths, list) and not isinstance(paths, tuple):
        paths = [paths]
    for p in paths:
        try:
            items = fs.listdir(p)
        except:
            continue

        for i in items:
            yield os.path.join(p, i)
        if recurse:
            subitems = ls([os.path.join(p, i) for i in items], True)
            for j in subitems:
                yield j
