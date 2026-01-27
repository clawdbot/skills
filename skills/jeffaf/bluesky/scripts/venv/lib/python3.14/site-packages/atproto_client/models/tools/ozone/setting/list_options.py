##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te
from pydantic import Field

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`tools.ozone.setting.listOptions`."""

    cursor: t.Optional[str] = None  #: Cursor.
    keys: te.Annotated[t.Optional[t.List[string_formats.Nsid]], Field(max_length=100)] = (
        None  #: Filter for only the specified keys. Ignored if prefix is provided.
    )
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    prefix: t.Optional[str] = None  #: Filter keys by prefix.
    scope: t.Optional[t.Union[t.Literal['instance'], t.Literal['personal'], str]] = 'instance'  #: Scope.


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    keys: te.NotRequired[
        t.Optional[t.List[string_formats.Nsid]]
    ]  #: Filter for only the specified keys. Ignored if prefix is provided.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    prefix: te.NotRequired[t.Optional[str]]  #: Filter keys by prefix.
    scope: te.NotRequired[t.Optional[t.Union[t.Literal['instance'], t.Literal['personal'], str]]]  #: Scope.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.setting.listOptions`."""

    options: t.List['models.ToolsOzoneSettingDefs.Option']  #: Options.
    cursor: t.Optional[str] = None  #: Cursor.
