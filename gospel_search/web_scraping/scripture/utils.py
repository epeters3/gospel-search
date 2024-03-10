import typing as t
import re
from urllib.parse import urlparse
import os
import json

from bs4 import BeautifulSoup

from gospel_search.web_scraping.config import SCRIPTURES_ROOT_URL
from gospel_search.web_scraping.utils import remove_query_string, get_normalized_text
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


def parse_url_ch_verses_str(s: str) -> t.Tuple[str, t.Iterable[str]]:
    """
    Parse Chapter/Verse strings as they exist in scripture reference
    URLs.
    """
    ch, verse_str = s.split(".")
    # Capture all single verse references in the string e.g. "6,9,21".
    verses = {m.groups()[0] for m in re.finditer(r"(?<!-|\d)(\d+)(?!-|\d)", verse_str)}
    # Capture all range verse references in the string e.g. "6-8".
    # Make a list of all the verses in the range specified by `verse_str`.
    verse_ranges = [m.groups() for m in re.finditer(r"(\d+)-(\d+)", verse_str)]
    for startv, endv in verse_ranges:
        for verse in range(int(startv), int(endv) + 1):
            verses.add(str(verse))
    return ch, verses


def parse_scripture_chapter_url(url: str) -> t.Dict[str, t.Any]:
    parsed = urlparse(url)
    path = parsed.path.split("/")
    # Filter out the cruft.
    path = [s for s in path if s not in ["", "study"]]
    assert len(path) == 4, f"chapter url path is length {len(path)}, expected length 4"
    return {
        "id": remove_query_string(url),
        "volume": path[1],
        "book_id": path[2],
        "ch": int(path[3]),
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
        logger.warning(
            f"scripture verses url '{path}' was not of "
            "length 4 as expected, skipping..."
        )
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
    matches = re.match(r"^([\da-zA-Z&\s\.]+)\s(\d+):(\d+)[-–]?(\d+)?", ref)

    if matches is None:
        return []

    # `ref` contains a scripture reference.
    book, ch, startv, endv = matches.groups()

    if book not in book_name_to_work:
        logger.warning(
            f"book '{book}' was not recognized as "
            "a valid scripture book name, skipping..."
        )
        return []

    if endv is None:
        # This is a reference for just one scripture.
        return [canonical_scripture_ref_to_id(book, ch, startv)]
    else:
        return [
            canonical_scripture_ref_to_id(book, ch, str(verse))
            for verse in range(int(startv), int(endv) + 1)
        ]
