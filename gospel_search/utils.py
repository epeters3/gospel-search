from itertools import zip_longest
import typing as t

import colorlog


handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
)

logger = colorlog.getLogger("gospel_search")
logger.addHandler(handler)
logger.setLevel("DEBUG")


def batcher(iterable: t.Iterable, n: int, fill_value=None):
    """
    Yields `iterable` in batches of size `n`, with any
    leftover space in the batch being populated by
    `fill_value`.

    source: https://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fill_value)
