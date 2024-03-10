import typing as t
import unicodedata
from urllib import parse

import requests
from bs4 import BeautifulSoup

from gospel_search.web_scraping.config import BODY_QUERY, RELATED_CONTENT_QUERY


def get_soup(url: str) -> BeautifulSoup:
    page = requests.get(url)
    # Raise exception for 4xx or 5xx HTTP codes.
    page.raise_for_status()

    return BeautifulSoup(page.content, features="lxml")


def get_normalized_text(soup: BeautifulSoup) -> str:
    """
    Get's the unicode normalized text under `soup`.
    Collects all strings under `soup` into one string.
    """
    text = ""
    for s in soup.stripped_strings:
        text += unicodedata.normalize("NFKC", s)
    return text


def get_all_urls_matching_query(
    dest_url: str, query: dict, root: str = ""
) -> t.List[str]:
    """
    Grabs the html document at `dest_url` and pulls the urls from all anchor
    tags matching `query`, which is a BeautifulSoup style query object.
    Prepends each url with `root`. Returns a list of all the urls.
    """
    soup = get_soup(dest_url)
    return [root + tag["href"] for tag in soup.find_all("a", query)]


def remove_query_string(url: str) -> str:
    parsed = parse.urlparse(url)
    parsed_no_query = parse.ParseResult(
        parsed.scheme, parsed.netloc, parsed.path, parsed.params, "", parsed.fragment
    )
    return parse.urlunparse(parsed_no_query)


def get_content_body(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Finds the div that holds the verses/paragraphs of the
    gospel library document.
    """
    bodies = soup.find_all(**BODY_QUERY)
    assert len(bodies) == 1, f"{len(bodies)} body blocks found when only 1 expected."
    return bodies[0]


def get_related_content(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Finds the related content section on the side of a gospel
    library document.
    """
    related_contents = soup.select(RELATED_CONTENT_QUERY)
    assert len(related_contents) == 1, (
        f"{len(related_contents)} Related Content sections"
        " found when 1 was expected."
    )
    return related_contents[0]

def bs_find(soup: BeautifulSoup, *queries: dict):
    """
    Searches through `soup` using the given queries. The first query will be tried first. If there is no match,
    the second query will be tried next, and so on.
    """
    res = None
    for query in queries:
        res = soup.find(**query)
        if res is not None:
            break
    return res