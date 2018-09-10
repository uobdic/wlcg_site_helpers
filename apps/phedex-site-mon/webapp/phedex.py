"""
    Wrap phedex calls and provide caching, e.g.
    If no cache: download phedex data
    If cache:
        - check last entry in cache
        - execute query for any new data
        - update cache
"""
