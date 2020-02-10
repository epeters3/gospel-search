import typing as t
import math

from fire import Fire
import requests

from gospel_search.pages.conference.utils import (
    get_all_conference_session_urls,
    get_all_talk_urls_for_conference_session,
)
from gospel_search.pages.conference.talk import ConferenceTalk
from gospel_search.pages.scripture.chapter import Chapter
from gospel_search.pages.scripture.utils import get_all_chapter_urls
from gospel_search.database.client import parent_doc_exists, db
from gospel_search.database.segment import write_segments
from gospel_search.utils import logger


def write_all_conference_talks(batch_size: int, limit: t.Optional[int], verbose: bool):
    """
    Grabs ALL conference talks from the church's website, parses
    them, and writes each paragraph of each talk to the database.
    """
    n_written = 0
    session_urls = get_all_conference_session_urls()
    for session_url in session_urls:
        talk_urls = get_all_talk_urls_for_conference_session(session_url)
        for talk_url in talk_urls:
            if limit is not None and n_written > limit:
                break
            talk_exists = parent_doc_exists(talk_url, "general-conference")
            logger.debug(f"'{talk_url}' exists: {talk_exists}")
            if not talk_exists:
                try:
                    try:
                        talk = ConferenceTalk(talk_url)
                    except requests.exceptions.HTTPError as e:
                        logger.warning(
                            f"'{talk_url}' returned with {e.response}, skipping..."
                        )
                        continue
                    write_segments(talk.to_segments(), batch_size)
                    if verbose:
                        logger.info(talk)
                    n_written += 1
                except Exception as e:
                    logger.error(f"failed to process and persist '{talk_url}'")
                    raise e


def write_all_scripture_chapters(
    batch_size: int, limit: t.Optional[int], verbose: bool
) -> None:
    """
    Grabs ALL scripture chapters from the church's website, parses
    them, and writes each verse of each chapter to the database.
    """
    n_written = 0
    for chapter_url in get_all_chapter_urls():
        if limit is not None and n_written > limit:
            break
        ch_exists = parent_doc_exists(chapter_url, "scriptures")
        logger.debug(f"'{chapter_url}' exists: {ch_exists}")
        if not ch_exists:
            try:
                try:
                    chapter = Chapter(chapter_url)
                except requests.exceptions.HTTPError as e:
                    logger.warning(
                        f"'{chapter_url}' returned with {e.response}, skipping..."
                    )
                    continue
                write_segments(chapter.to_segments(), batch_size)
                if verbose:
                    logger.info(chapter)
                n_written += 1
            except Exception as e:
                logger.error(f"failed to process and persist '{chapter_url}'")
                raise e


def populate(
    batch_size: int = 32,
    overwrite: bool = False,
    limit: t.Optional[int] = None,
    log_level: str = "INFO",
    verbose: bool = False,
) -> None:
    """
    Writes all conference talks and all scriptures to the database.

    Parameters
    ----------
    batch_size
        The maximum number of segments to write to the database in
        each batch. If a talk or scripture chapter has less
        paragraphs/verses than `batch_size`, only that number will
        be written at once for that talk or chapter.
    overwrite
        If `True`, all segments will be removed, and a fresh write will
        take place. If `False`, segments will only be written to the db
        for documents that are not referenced yet in the db.
    limit
        If supplied, the number of documents written to the database will
        not exceed `limit`. Useful for testing and debugging.
    log_level
        The level to set logging to. One of
        `["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]`.
    verbose
        If `True`, general info about each talk or chapter will be outputted
        after each successful parse.
    """
    if overwrite:
        # Delete all segments in the collection.
        logger.info("deleteing all documents in the segments collection...")
        db.segments.delete_many({})

    logger.setLevel(log_level)
    sub_limit = math.ceil(limit / 2) if limit is not None else None
    # write_all_conference_talks(batch_size, sub_limit, verbose)
    write_all_scripture_chapters(batch_size, sub_limit, verbose)


if __name__ == "__main__":
    # print(
    #     ConferenceTalk(
    #         "https://www.churchofjesuschrist.org/study/general-conference/2019/04/56rasband?lang=eng"
    #     )
    # )
    # print(
    #     Chapter(
    #         "https://www.churchofjesuschrist.org/study/scriptures/bofm/2-ne/1?lang=eng"
    #     )
    # )
    Fire(populate)
