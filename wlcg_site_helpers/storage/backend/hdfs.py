from snakebite.client import AutoConfigClient
import pandas as pd

fs = AutoConfigClient()

def ls(paths=['/'], recursive=False):
    if not isinstance(paths, list) and not isinstance(paths, tuple):
        paths = [paths]
    data = [dict(size=p['length'], path=p['path'], ftype=p['file_type'], date=p['modification_time']) for p in fs.ls(paths, recursive)]
    df = pd.DataFrame(data)
    df = df.reindex(['size', 'path', 'ftype', 'date'], axis=1)
    df['size'] = df['size'].astype(int)
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    # ignore current uploads
    df = df[~df.path.str.endswith('.upload')]
    return df