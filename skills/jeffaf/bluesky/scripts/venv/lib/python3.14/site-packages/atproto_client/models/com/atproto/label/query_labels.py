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
    """Parameters model for :obj:`com.atproto.label.queryLabels`."""

    uri_patterns: t.List[
        str
    ]  #: List of AT URI patterns to match (boolean 'OR'). Each may be a prefix (ending with '*'; will match inclusive of the string leading to '*'), or a full URI.
    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=250)] = None  #: Limit.
    sources: t.Optional[t.List[string_formats.Did]] = None  #: Optional list of label sources (DIDs) to filter on.


class ParamsDict(t.TypedDict):
    uri_patterns: t.List[
        str
    ]  #: List of AT URI patterns to match (boolean 'OR'). Each may be a prefix (ending with '*'; will match inclusive of the string leading to '*'), or a full URI.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    sources: te.NotRequired[
        t.Optional[t.List[string_formats.Did]]
    ]  #: Optional list of label sources (DIDs) to filter on.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.label.queryLabels`."""

    labels: t.List['models.ComAtprotoLabelDefs.Label']  #: Labels.
    cursor: t.Optional[str] = None  #: Cursor.
