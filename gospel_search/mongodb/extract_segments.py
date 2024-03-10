import typing as t

from fire import Fire

from gospel_search.utils import logger
from gospel_search.mongodb.client import db
from gospel_search.web_scraping.conference.talk import ConferenceTalk
from gospel_search.web_scraping.scripture.chapter import Chapter
from gospel_search.web_scraping.page import Page
from gospel_search.mongodb.segment import write_segments


def extract_segments(limit: t.Optional[int] = None, log_level: str = "INFO"):
    """
    Takes all conference talks and scripture chapters in the pages
    collection of the database and extracts all the segments from
    them, including cleaned text, meta-data, and the references of
    each segment.
    """
    n_written = 0
    logger.setLevel(log_level)

    # First delete all segments in the collection.
    logger.info("deleting all documents in the segments collection...")
    db.segments.delete_many({})

    for page_dict in db.pages.find({}):
        if limit is not None and n_written >= limit:
            break

        page = Page(**page_dict)
        if "session" in page._id:
            logger.info(
                f"Skipping page {page._id} because it appears to be a conference session landing page"
            )
            continue
        if "video" in page._id:
            logger.info(f"Skipping page {page._id} because it appears to be a video with no text")
            continue
        if page.doc_type == "scriptures":
            segmentable = Chapter(page)
        elif page.doc_type == "general-conference":
            segmentable = ConferenceTalk(page)
        else:
            raise ValueError(f"unsupported doc_type '{page.doc_type}'")

        logger.debug(segmentable)

        write_segments(segmentable.to_segments())
        n_written += 1


if __name__ == "__main__":
    Fire(extract_segments)
