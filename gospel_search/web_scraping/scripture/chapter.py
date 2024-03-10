import typing as t
import unicodedata

from bs4 import BeautifulSoup, NavigableString

from gospel_search.utils import logger
from gospel_search.mongodb.segment import Segment, Segmentable
from gospel_search.web_scraping.utils import (
    get_content_body,
    get_related_content,
)
from gospel_search.web_scraping.scripture.utils import (
    parse_scripture_chapter_url,
    book_map,
)
from gospel_search.web_scraping.page import Page


class Verse:

    FOOTNOTE_LINK_QUERY = {"name": "a", "class": "study-note-ref"}

    def __init__(self, v_soup: BeautifulSoup):
        """
        Takes a BeautifulSoup object for the `<p/>` tag of
        a scripture chapter verse and processes it into
        the verse's text and links.

        Parameters
        ----------
        v_soup
            The `BeautifulSoup` object corresponding to the verse
            in question (just the `<p/>` tag).
        """
        # TODO: this is not extracting any links currently.
        self.links = []

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

    def __init__(self, page: Page) -> None:
        logger.info(f"processing {page._id}...")
        self.url = page._id
        self.soup = BeautifulSoup(page.html, features="lxml")

        attrs = parse_scripture_chapter_url(self.url)
        self.id: str = attrs["id"]
        self.volume: str = attrs["volume"]
        self.book_id: str = attrs["book_id"]
        self.ch: int = attrs["ch"]
        self.book_name: str = book_map[self.book_id]["names"][0]

        self._set_segments()

    def _set_segments(self) -> None:
        self.verses: t.List[Verse] = []
        self.nlinks = 0
        body = get_content_body(self.soup)

        verse_tags = body.find_all(**self.VERSES_IN_BODY_QUERY)
        for verse_tag in verse_tags:
            verse = Verse(verse_tag)
            self.nlinks += len(verse.links)
            self.verses.append(verse)

    def to_segments(self) -> t.List[Segment]:
        return [
            Segment(
                _id=f"{self.id}.{i+1}",
                parent_id=self.id,
                num=(i + 1),
                doc_type="scriptures",
                text=v.text,
                name=f"{self.book_name} {self.ch}",
                links=v.links,
                chapter=self.ch,
                book_id=self.book_id,
                volume=self.volume,
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
