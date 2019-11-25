from dataclasses import dataclass

from mashumaro import DataClassDictMixin


@dataclass(frozen=True)
class ReleaseRankmiResponse(DataClassDictMixin):
    ok: bool
    status: str
    api_message: str
    app_message: str


@dataclass(frozen=True)
class ReleaseProjectResponse(DataClassDictMixin):
    ok: bool
    status: str
    message: str
