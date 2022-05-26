import typing as t

from pydantic import BaseModel

LogLevel = t.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class PullPagesConfig(BaseModel):
    overwrite: bool = False
    limit: t.Optional[int] = None
    log_level: LogLevel = "INFO"


class ExtractSegmentsConfig(BaseModel):
    limit: t.Optional[int] = None
    log_level: LogLevel = "INFO"


class ComputeEmbeddingsConfig(BaseModel):
    overwrite: bool = False


class ImportDocsConfig(BaseModel):
    overwrite: bool = False
    log_level: LogLevel = "INFO"
