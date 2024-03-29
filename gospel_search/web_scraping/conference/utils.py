from datetime import datetime
import typing as t
from urllib.parse import urlparse

from gospel_search.web_scraping.utils import (
    get_all_urls_matching_query,
    remove_query_string,
)
from gospel_search.web_scraping.config import ALL_CONFERENCES_URL, CHURCH_ROOT_URL


def is_conference_talk_url(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path.split("/")
    if path[1] != "study":
        return False
    if path[2] != "general-conference":
        return False
    if len(path[3]) != 4:
        # We assume this is not a conference year
        return False
    if len(path[4]) != 2:
        # We assume this is not a conference month
        return False
    if path[-2] == "media":
        # This is likely a link to media associated
        # with the conference session, and not a talk
        return False
    if "session" in path[5] or "video" in path[5]:
        # This is likely a session landing page with no
        # actual talk in it, or just a video with no text
        # content written on the page i.e. not an official
        # conference talk but just a piece of shared media,
        # like a church video.
        return False
    return True


CONFERENCE_SESSION_LINK_QUERY = {"class": "year-line__link"}
CONFERENCE_TALK_LINK_QUERY = {
    "class": "list-tile",
    "href": is_conference_talk_url,
}


def parse_conference_talk_url(url: str) -> t.Dict[str, t.Any]:
    parsed = urlparse(url)
    path = parsed.path.split("/")
    # Filter out the cruft.
    path = [s for s in path if s not in ["", "study"]]
    assert len(path) == 4, f"{path} was not of length 4 as expected"

    year = path[1]
    assert len(year) == 4, f"{year} is not of length 4"

    month = path[2]
    assert len(month) == 2, f"{month} is not of length 2"

    talk_id = path[3]

    return {
        "id": remove_query_string(url),
        "volume": int(year),
        "work": int(month),
        # The name of the talk as it exists in the talk's url
        "parent_doc": talk_id,
    }


def get_all_conference_session_urls() -> t.List[str]:
    start_year = 1971
    current_year = datetime.now().year
    current_month = datetime.now().month
    urls = []
    for year in range(start_year, current_year + 1):
        for month in [4, 10]:
            if year == current_year and month >= current_month:
                # This conference may not be available yet.
                break
            urls.append(f"{ALL_CONFERENCES_URL}/{year}/{month:02d}")

    return urls


def get_all_talk_urls_for_conference_session(session_url: str) -> t.List[str]:
    return get_all_urls_matching_query(
        session_url, CONFERENCE_TALK_LINK_QUERY, CHURCH_ROOT_URL
    )


def get_all_conference_talk_urls() -> t.Iterable[str]:
    for session_url in get_all_conference_session_urls():
        for talk_url in get_all_talk_urls_for_conference_session(session_url):
            yield talk_url
