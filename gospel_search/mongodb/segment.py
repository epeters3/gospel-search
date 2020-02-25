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
        *,
        _id: str,
        doc_type: "str",
        text: str,
        name: str,
        links: t.List[str],
        **other_props,
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
        name:
            The segment's human readable name. For a scripture, this would be something
            like "1 Nephi 12:3". For a conference talk, this would be something like
            "The Joy of Spiritual Survival" (the name of the conference talk).
        links:
            A list of `_id`s of other segments that this segment links to.
        **other_props:
            The other properties that will be set on the segment. These can vary by
            segment type like chapter, work, and volume for a scripture segment, or
            talk, month, year for a conference talk paragraph.
        """
        self.d = {
            "_id": _id,
            "doc_type": doc_type,
            "text": text,
            "name": name,
            "links": links,
            **other_props,
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


def write_segments(segments: t.List[Segment]) -> None:
    """
    Writes `segments` to the database all as one batch.
    """
    db.segments.insert_many([segment.d for segment in segments])
