from snakebite.client import AutoConfigClient
import pandas as pd

fs = AutoConfigClient()

def ls(paths=['/'], recursive=False):
    if not isinstance(paths, list) and not isinstance(paths, tuple):
        paths = [paths]
    data = [dict(size=p['length'], path=p['path']) for p in fs.ls(paths, recursive)]
    df = pd.DataFrame(data)
    df = df.reindex(['size', 'path'], axis=1)
    return df