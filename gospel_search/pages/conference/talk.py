import re
import typing as t
import unicodedata

from bs4 import BeautifulSoup, NavigableString

from gospel_search.pages.utils import (
    get_soup,
    get_content_body,
    get_related_content,
    find_scripture_refs,
)
from gospel_search.pages.scripture.utils import parse_scripture_verses_url
from gospel_search.pages.conference.utils import parse_conference_talk_url
from gospel_search.mongodb.segment import Segment, Segmentable
from gospel_search.utils import logger


class Paragraph:

    OLD_SCRIPTURE_LINK_QUERY = {"name": "a", "class": "scripture-ref"}
    NEW_SCRIPTURE_LINK_QUERY = {"name": "a", "class": "note-ref"}

    def __init__(self, p_soup: BeautifulSoup, rc_soup: BeautifulSoup):
        """
        Takes a BeautifulSoup object for the `<p/>` tag of
        a conference talk paragraph and processes it into
        the paragraph's text and links.

        Parameters
        ----------
        p_soup
            The `BeautifulSoup` object corresponding to the paragraph
            in question (just the `<p/>` tag).
        rc_soup
            The `BeautifulSoup` object corresponding to the Related
            Content section of the talk.
        """
        self.links: t.List[str] = []

        # Capture any old-style scripture links in this paragraph where
        # the scripture reference and url are embedded right in the paragraph.
        for old_anchor in p_soup.find_all(**self.OLD_SCRIPTURE_LINK_QUERY):
            self.links += parse_scripture_verses_url(old_anchor["href"])

        # Capture any new-style scripture links in this paragraph where
        # the actual scripture reference is in the "Related Content" section.
        self.links += find_scripture_refs(
            p_soup, self.NEW_SCRIPTURE_LINK_QUERY, rc_soup
        )

        # Collect the text for the paragraph, ignoring superscript
        # footnote numbers.
        self.text = ""
        for child in p_soup.descendants:
            if isinstance(child, NavigableString):
                if child.parent.name == "sup":
                    if any(class_ == "marker" for class_ in child.parent["class"]):
                        continue
                self.text += unicodedata.normalize("NFKC", child)


class ConferenceTalk(Segmentable):

    NAME_QUERY = {"id": "title1"}
    AUTHOR_QUERYS = [{"id": "author1"}, {"id": "p1"}]
    PARAGRAPHS_IN_BODY_QUERY = {"name": "p"}

    def __init__(self, talk_url: str) -> None:
        logger.info(f"processing '{talk_url}'...")
        self.url = talk_url
        self.soup = get_soup(self.url)

        attrs = parse_conference_talk_url(self.url)
        self.id: str = attrs["id"]
        self.year: int = attrs["volume"]
        self.month: int = attrs["work"]
        self.url_name: str = attrs["parent_doc"]

        self.name = self.soup.find(**self.NAME_QUERY).string
        self._set_author()
        self._set_segments()

    def _set_author(self) -> None:
        tag = self.soup.find(**self.AUTHOR_QUERYS[0])
        if tag is None:
            tag = self.soup.find(**self.AUTHOR_QUERYS[1])
        # Keep just the author in "<By> author"
        self.author = re.sub(r"^[B|b]y\s", "", tag.string)

    def _set_segments(self) -> None:
        self.paragraphs: t.List[Paragraph] = []
        self.nlinks = 0

        body = get_content_body(self.soup)

        # The related content section has the text corresponding
        # to new-style link footnotes.
        related_content = get_related_content(self.soup)

        p_tags = body.find_all(**self.PARAGRAPHS_IN_BODY_QUERY)
        for p in p_tags:
            if not p.parent.name == "figcaption":
                # We don't want text that serves as the
                # caption to a figure.
                paragraph = Paragraph(p, related_content)
                self.nlinks += len(paragraph.links)
                self.paragraphs.append(paragraph)

    def to_segments(self) -> t.List[Segment]:
        return [
            Segment(
                f"{self.id}.{i+1}",
                "general-conference",
                p.text,
                p.links,
                self.url_name,
                self.month,
                self.year,
            )
            for i, p in enumerate(self.paragraphs)
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
