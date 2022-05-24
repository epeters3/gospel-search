import typing as t

from pydantic import BaseModel


class PullPagesConfig(BaseModel):
    overwrite: bool = False
    limit: t.Optional[int] = None
    log_level: t.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"


class ExtractSegmentsConfig(BaseModel):
    overwrite: bool = False
    limit: t.Optional[int] = None
    log_level: t.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"


class ComputeEmbeddingsConfig(BaseModel):
    overwrite: bool = False


class ImportDocsConfig(BaseModel):
    overwrite: bool = False
    log_level: t.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
