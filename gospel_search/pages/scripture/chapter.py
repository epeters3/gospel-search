import typing as t
import unicodedata

from bs4 import BeautifulSoup, NavigableString

from gospel_search.utils import logger
from gospel_search.database.segment import Segment, Segmentable
from gospel_search.pages.utils import (
    get_soup,
    get_content_body,
    get_related_content,
    find_scripture_refs,
)
from gospel_search.pages.scripture.utils import (
    parse_scripture_chapter_url,
    book_map,
)


class Verse:

    FOOTNOTE_LINK_QUERY = {"name": "a", "class": "study-note-ref"}

    def __init__(self, v_soup: BeautifulSoup, rc_soup: BeautifulSoup):
        """
        Takes a BeautifulSoup object for the `<p/>` tag of
        a scripture chapter verse and processes it into
        the verse's text and links.

        Parameters
        ----------
        v_soup
            The `BeautifulSoup` object corresponding to the verse
            in question (just the `<p/>` tag).
        rc_soup
            The `BeautifulSoup` object corresponding to the Related
            Content section of the talk.
        """
        self.links = find_scripture_refs(v_soup, self.FOOTNOTE_LINK_QUERY, rc_soup)

        # Collect all the text for the verse, excluding the text
        # for footnote letters and verse numbers.
        self.text = ""
        for child in v_soup.descendants:
            if isinstance(child, NavigableString):
                if child.parent.name in ["sup", "span"]:
                    if any(
                        class_ in ["verse-number", "marker"]
                        for class_ in child.parent["class"]
                    ):
                        continue
                self.text += unicodedata.normalize("NFKC", child)


class Chapter(Segmentable):
    """
    Gets and extracts data about a chapter of scripture.
    """

    VERSES_IN_BODY_QUERY = {"name": "p", "class": "verse"}

    def __init__(self, ch_url: str) -> None:
        logger.info(f"processing '{ch_url}'...")
        self.url = ch_url
        self.soup = get_soup(self.url)
        attrs = parse_scripture_chapter_url(self.url)
        self.id: str = attrs["id"]
        self.volume: str = attrs["volume"]
        self.work: str = attrs["work"]
        self.name: str = book_map[self.work]["names"][0]
        self.ch: int = attrs["parent_doc"]
        self._set_segments()

    def _set_segments(self) -> None:
        self.verses: t.List[Verse] = []
        self.nlinks = 0
        body = get_content_body(self.soup)
        related_content = get_related_content(self.soup)

        verse_tags = body.find_all(**self.VERSES_IN_BODY_QUERY)
        for verse_tag in verse_tags:
            verse = Verse(verse_tag, related_content)
            self.nlinks += len(verse.links)
            self.verses.append(verse)

    def to_segments(self) -> t.List[Segment]:
        return [
            Segment(
                f"{self.id}.{i+1}",
                "scriptures",
                v.text,
                v.links,
                self.ch,
                self.work,
                self.volume,
            )
            for i, v in enumerate(self.verses)
        ]

    def __str__(self) -> str:
        return f"""
Chapter: "{self.id}"
    url: {self.url}
    length: {len(self.verses)} verses
    nlinks: {self.nlinks}

1st verse:
{self.verses[0].text}
        """
