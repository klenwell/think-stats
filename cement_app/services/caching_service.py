from functools import lru_cache


# TODO: This can be removed when app upgrades to Python 3.8. It provides this function.
# Source: https://stackoverflow.com/a/16099881/1093087
def cached_property(f):
    return property(lru_cache()(f))
