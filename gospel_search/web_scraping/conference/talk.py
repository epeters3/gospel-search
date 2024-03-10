import re
import typing as t
import unicodedata

from bs4 import BeautifulSoup, NavigableString

from gospel_search.web_scraping.utils import (
    bs_find,
    get_content_body,
    get_related_content,
)
from gospel_search.web_scraping.scripture.utils import (
    parse_scripture_verses_url,
)
from gospel_search.web_scraping.conference.utils import parse_conference_talk_url
from gospel_search.mongodb.segment import Segment, Segmentable
from gospel_search.utils import logger
from gospel_search.web_scraping.page import Page


class Paragraph:

    OLD_SCRIPTURE_LINK_QUERY = {"name": "a", "class_": "scripture-ref"}
    NEW_SCRIPTURE_LINK_QUERY = {"name": "a", "class_": "note-ref"}

    def __init__(self, p_soup: BeautifulSoup):
        """
        Takes a BeautifulSoup object for the `<p/>` tag of
        a conference talk paragraph and processes it into
        the paragraph's text and links.

        Parameters
        ----------
        p_soup
            The `BeautifulSoup` object corresponding to the paragraph
            in question (just the `<p/>` tag).
        """
        self.links: t.List[str] = []

        # Capture any old-style scripture links in this paragraph where
        # the scripture reference and url are embedded right in the paragraph.
        for old_anchor in p_soup.find_all(**self.OLD_SCRIPTURE_LINK_QUERY):
            self.links += parse_scripture_verses_url(old_anchor["href"])

        # Collect the text for the paragraph, ignoring superscript
        # footnote numbers.
        self.text = ""
        for child in p_soup.descendants:
            if isinstance(child, NavigableString):
                if child.parent.name == "sup":
                    if any(class_ == "marker" for class_ in child.parent.get("class", [])):
                        continue
                self.text += unicodedata.normalize("NFKC", child)


class ConferenceTalk(Segmentable):

    NAME_QUERIES = [{"name": "h1", "id": "title1"}, {"name": "h1", "id": "p1"}, {"name": "h1", "id": "p4"}, {"name": "h1", "id": "title56"}]
    AUTHOR_QUERIES = [{"name": "p", "id": "author1"}, {"name": "p", "id": "p1"}, {"name": "p", "class_": "author-name"}]
    PARAGRAPHS_IN_BODY_QUERY = {"name": "p"}

    def __init__(self, page: Page) -> None:
        logger.info(f"processing {page._id}...")
        self.url = page._id
        self.soup = BeautifulSoup(page.html, features="lxml")

        attrs = parse_conference_talk_url(self.url)
        self.id: str = attrs["id"]
        self.year: int = attrs["volume"]
        self.month: int = attrs["work"]
        self.url_name: str = attrs["parent_doc"]

        self.name = bs_find(self.soup, *self.NAME_QUERIES).string
        self._set_author()
        self._set_segments()

    def _set_author(self) -> None:
        tag = bs_find(self.soup, *self.AUTHOR_QUERIES)
        if tag is None or not tag.text:
            raise Exception(f"Could not find conference talk author string using any known query.")
        # Keep just the author in "<By> author"
        self.author = re.sub(r"^[B|b]y\s", "", tag.text)

    def _set_segments(self) -> None:
        self.paragraphs: t.List[Paragraph] = []
        self.nlinks = 0

        body = get_content_body(self.soup)

        p_tags = body.find_all(**self.PARAGRAPHS_IN_BODY_QUERY)
        for p in p_tags:
            if not p.parent.name == "figcaption":
                # We don't want text that serves as the
                # caption to a figure.
                paragraph = Paragraph(p)
                self.nlinks += len(paragraph.links)
                self.paragraphs.append(paragraph)

    def to_segments(self) -> t.List[Segment]:
        return [
            Segment(
                _id=f"{self.id}.{i+1}",
                parent_id=self.id,
                num=(i + 1),
                doc_type="general-conference",
                text=p.text,
                name=self.name,
                links=p.links,
                talk_id=self.url_name,
                month=self.month,
                year=self.year,
            )
            for i, p in enumerate(self.paragraphs)
            # There is an empty paragraph here and there, like in
            # the church's statistical reports.
            if p.text != "" and p.text != " "
        ]

    def __str__(self) -> str:
        return f"""
"{self.name}"
author: {self.author}
    date: {self.month}/{self.year}
    url: {self.url}
    url_name: {self.url_name}
    id: {self.id}
    length: {len(self.paragraphs)} paragraphs
    nlinks: {self.nlinks}

1st paragraph:
{self.paragraphs[0].text}
        """
