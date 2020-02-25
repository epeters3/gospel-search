import requests

from gospel_search.utils import logger


class Page:
    """
    A class that can take a page URL, get the page,
    and export it as JSON with a little associated
    metadata.
    """

    def __init__(self, _id: str, doc_type: str, html: str = None) -> None:
        """
        `doc_type` is the document type, one of `["general-conference", "scriptures"]`.
        """
        logger.info(f"pulling '{_id}'...")
        self._id = _id
        self.doc_type = doc_type
        if html is None:
            res = requests.get(self._id)
            # Raise exception for 4xx or 5xx HTTP codes.
            res.raise_for_status()
            self.html = res.text
        else:
            self.html = html

    def to_json_document(self) -> dict:
        """
        Return object as it should be in MongoDB document form.
        """
        return {"_id": self._id, "doc_type": self.doc_type, "html": self.html}
