import typing as t
import re
from urllib.parse import urlparse
import os
import json

from gospel_search.pages.config import SCRIPTURES_ROOT_URL
from gospel_search.utils import logger

# Maps scripture book ids like `dc` to their attributes
# like canonical names ("D&C", "Doctrine and Covenants")
book_map = json.load(
    open(os.path.join(os.path.dirname(__file__), "scripture_book_map.json"))
)
# Maps canonical names (e.g. "D&C", "Doctrine and Covenants")
# to their id name (the "work") e.g. "dc".
book_name_to_work = {}
for work, attrs in book_map.items():
    for name in attrs["names"]:
        book_name_to_work[name] = work


def get_all_chapter_urls() -> t.List[str]:
    """
    Returns the URLs for all chapters of all books in all
    volumes of the standard works.
    """
    urls: t.List[str] = []
    for work, attrs in book_map.items():
        for ch in range(1, attrs["n_ch"] + 1):
            urls.append(f"{SCRIPTURES_ROOT_URL}/{attrs['volume']}/{work}/{ch}")
    return urls


def parse_url_ch_verses_str(s: str) -> t.Tuple[str, t.List[str]]:
    """
    Parse Chapter/Verse strings of the format `5.13-18` (chapter
    5, verses 13 through 18). This is how they are formatted in
    scripture URLs.
    """
    ch, verse_str = s.split(".")
    if "-" in verse_str:
        # Multiple verses are referenced (e.g. "6-8"). Make a list of
        # all the verses in the range specified by `verse_str`.
        startv, endv = verse_str.split("-")
        verses = [str(i) for i in range(int(startv), int(endv) + 1)]
    else:
        # Only one verse is referenced.
        verses = [verse_str]
    return ch, verses


def parse_scripture_chapter_url(url: str) -> t.Dict[str, t.Any]:
    parsed = urlparse(url)
    path = parsed.path.split("/")
    # Filter out the cruft.
    path = [s for s in path if s not in ["", "study"]]
    assert len(path) == 4, f"chapter url path is length {len(path)}, expected length 4"
    return {
        "id": "/" + "/".join(path),
        "volume": path[1],
        "work": path[2],
        "parent_doc": int(path[3]),
    }


def parse_scripture_verses_url(url: str) -> t.List[str]:
    """
    Parses a link to a one or more scripture verses
    and creates a list of `_id`s for each verse the
    link references.
    """
    parsed = urlparse(url)
    path = parsed.path.split("/")

    # Filter out the cruft.
    path = [s for s in path if s not in ["", "study"]]
    if len(path) != 4:
        logger.warning(f"{path} was not of length 4 as expected, skipping...")
        return []

    ch_verses_str = path[3]  # e.g. "3.8-9" (ch. 3, verses 8-9)
    if "." not in ch_verses_str:
        # This url likely references an entire chapter.
        # TODO: If this happens, create an `_id` for every verse
        # in the chapter?
        return []
    ch, verses = parse_url_ch_verses_str(ch_verses_str)

    return ["/" + "/".join([*path[:-1], ch]) + f".{verse_num}" for verse_num in verses]


def canonical_scripture_ref_to_id(book_name: str, ch: str, verse: str) -> str:
    """
    E.g. turns `{book_name: "1 Nephi", ch: "3", verse: "5"}`
    into a scripture `_id`.
    """
    work = book_name_to_work[book_name]
    attrs = book_map[work]
    return f"/scriptures/{attrs['volume']}/{work}/{ch}.{verse}"


def parse_canonical_scriptures_ref(ref: str) -> t.List[str]:
    """
    Parses the canonical scripture references like "3 Nephi 17:3-5"
    into a list of `_id`s for each verse in the reference. Returns
    an empty list if this function determines `ref` is not a reference to
    a scripture.
    """
    # Parse the scripture reference into book, chapter, and verse(s).
    matches = re.match(r"^([\da-zA-Z&\s\.]+)\s(\d+):(\d+)-?(\d+)?", ref,)

    if matches is None:
        return []

    # `ref` contains a scripture reference.
    book, ch, startv, endv = matches.groups()
    if endv is None:
        # This is a reference for just one scripture.
        return [canonical_scripture_ref_to_id(book, ch, startv)]
    else:
        return [
            canonical_scripture_ref_to_id(book, ch, str(verse))
            for verse in range(int(startv), int(endv) + 1)
        ]
