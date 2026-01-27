##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`tools.ozone.moderation.getSubjects`."""

    subjects: t.List[str] = Field(min_length=1, max_length=100)  #: Subjects.


class ParamsDict(t.TypedDict):
    subjects: t.List[str]  #: Subjects.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.moderation.getSubjects`."""

    subjects: t.List['models.ToolsOzoneModerationDefs.SubjectView']  #: Subjects.
