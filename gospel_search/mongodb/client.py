from pymongo import MongoClient

from gospel_search.pages.conference.utils import parse_conference_talk_url
from gospel_search.pages.scripture.utils import parse_scripture_chapter_url
from gospel_search.utils import logger

client = MongoClient()
db = client.gospel_search


def parent_doc_exists(parent_doc_url: str, doc_type: str) -> bool:
    """
    Used to check if a scripture chapter or conference talk
    is already referenced in the database.
    
    Parameters
    ----------
    parent_doc_url
        The conference talk URL or scripture chapter URL.
    doc_type
        One of `["general-conference", "scriptures"]`. Whether the
        `parent_doc_url` corresponds to a conference talk
        or scripture chapter.
    """
    if doc_type == "general-conference":
        attrs = parse_conference_talk_url(parent_doc_url)
    elif doc_type == "scriptures":
        attrs = parse_scripture_chapter_url(parent_doc_url)
    else:
        raise ValueError("unsupported doc_type")

    query = {
        "doc_type": doc_type,
        "work": attrs["work"],
        "volume": attrs["volume"],
        "parent_doc": attrs["parent_doc"],
    }

    logger.debug(query)

    if db.segments.find_one(query) is None:
        return False
    else:
        return True
