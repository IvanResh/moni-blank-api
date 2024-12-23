from itertools import islice


def get_key(obj, *path, default=None):  # noqa: C901
    rv = obj
    if rv is None:
        return default
    for x in path:
        if isinstance(x, str):
            rv = rv.get(x)
        elif isinstance(x, int):
            try:
                if isinstance(rv, list):
                    rv = rv[x]
                else:
                    rv = rv.get(x)
            except AttributeError:
                pass
        elif isinstance(x, tuple):
            rv = rv.get(x)
        else:
            raise ValueError(f"Bad path: {path}")

        if rv is None:
            return default

    return rv


def coalesce(*args):
    return next((a for a in args if a is not None), None)


def chunk_dict(data: dict, size: int):
    it = iter(data)
    for i in range(0, len(data), size):
        yield {k: data[k] for k in islice(it, size)}
