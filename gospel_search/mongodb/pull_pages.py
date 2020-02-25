import typing as t
import math

from fire import Fire
import requests

from gospel_search.utils import logger
from gospel_search.pages.conference.utils import get_all_conference_talk_urls
from gospel_search.pages.scripture.utils import get_all_chapter_urls
from gospel_search.pages.page import Page
from gospel_search.mongodb.client import db


def pull_pages_for_type(
    limit: t.Optional[int],
    doc_type: str,
    doc_urls: t.Iterable[str],
    existing_doc_ids: t.Set[str],
) -> None:
    """
    `existing_doc_ids` is a set of the `_id`s of all pages that already
    exist in the pages collection of the database.
    """
    n_written = 0

    for doc_url in doc_urls:
        if limit is not None and n_written >= limit:
            break

        if doc_url in existing_doc_ids:
            # We already have this page in the database
            continue

        try:
            page = Page(doc_url, doc_type)
        except requests.exceptions.HTTPError as e:
            logger.warning(f"'{doc_url}' returned with {e.response}, skipping...")
            continue

        db.pages.insert_one(page.to_json_document())
        n_written += 1


def pull_pages(
    overwrite: bool = False, limit: t.Optional[int] = None, log_level: str = "INFO",
):
    """
    Writes the raw HTML content of all conference talks and scriptures to the database.

    Parameters
    ----------
    overwrite
        If `True`, all pages will be removed, and a fresh write will
        take place. If `False`, pages will only be written to the db
        for documents that are not referenced yet in the db.
    limit
        If supplied, the number of documents written to the database will
        not exceed `limit`. Useful for testing and debugging.
    log_level
        The level to set logging to. One of
        `["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]`.
    """
    logger.setLevel(log_level)

    if overwrite:
        # Delete all HTML pages in the collection.
        logger.info("deleting all documents in the pages collection...")
        db.pages.delete_many({})

    sub_limit = math.ceil(limit / 2) if limit is not None else None
    existing_doc_ids = set(doc["_id"] for doc in db.pages.find({}, {"_id": 1}))

    pull_pages_for_type(
        sub_limit,
        "general-conference",
        get_all_conference_talk_urls(),
        existing_doc_ids,
    )
    pull_pages_for_type(
        sub_limit, "scriptures", get_all_chapter_urls(), existing_doc_ids
    )


if __name__ == "__main__":
    Fire(pull_pages)
