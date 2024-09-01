import typing as t
from abc import ABC, abstractmethod
from collections import defaultdict

from tqdm import tqdm
import numpy as np

from gospel_search.mongodb.client import db
from gospel_search.utils import logger


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
        parent_id: str,
        num: int,
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
        parent_id:
            The URL of the segment's parent (i.e. conference talk or scripture chapter)
            document.
        num:
            The verse number or conference talk paragraph number.
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
            "parent_id": parent_id,
            "num": num,
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


def get_all_segments():
    """
    Streams all segments from MongoDB.
    """
    segments_collection = db.segments
    for segment in tqdm(
        segments_collection.find(), total=segments_collection.count_documents(filter={})
    ):  
        segment.pop("embedding")
        yield segment
