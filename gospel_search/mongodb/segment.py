import typing as t
from abc import ABC, abstractmethod

from gospel_search.mongodb.client import db


class Segment:
    """
    Represents either a verse or scripture or
    a paragraph of a conference talk. Can
    interface directly with the database e.g.
    write itself to the database, etc.
    """

    def __init__(
        self,
        _id: str,
        doc_type: "str",
        text: str,
        links: t.List[str],
        parent_doc: t.Union[str, int],
        work: t.Union[str, int],
        volume: t.Union[str, int],
    ) -> None:
        """
        Parameters
        ----------
        _id:
            The human readable id that globally identifies this segment.
        doc_type:
            One of `["general-conference", "scriptures"]`. What type of segment it is.
        text:
            The actual text of the segment.
        links:
            A list of `_id`s of other segments that this segment links to.
        parent_doc:
            The chapter number or conference talk name the segment is a part of.
        work:
            The book or conference month the segment is a part of.
        volume:
            The volume of scripture or conference year the segment is a part of.
        """
        self.d = {
            "_id": _id,
            "doc_type": doc_type,
            "text": text,
            "links": links,
            "parent_doc": parent_doc,
            "work": work,
            "volume": volume,
        }


class Segmentable(ABC):
    """
    Represents an object that can be persisted
    to the database in the `segments` collection.
    """

    @abstractmethod
    def to_segments(self) -> t.List[Segment]:
        """
        Should take the object's segments, whether
        they be scripture verses or conference talk
        paragraphs, and turn them into a list of
        instances of the `Segment` class.
        """
        raise NotImplementedError


def write_segments(segments: t.List[Segment], batch_size: int) -> None:
    """
    Writes `segments` to the database, writing as many as
    `batch_size` at a time on each db call.
    """
    db.segments.insert_many([segment.d for segment in segments])
