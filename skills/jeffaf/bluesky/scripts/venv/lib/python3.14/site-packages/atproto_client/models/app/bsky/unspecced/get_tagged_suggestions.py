##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`app.bsky.unspecced.getTaggedSuggestions`."""


class ParamsDict(t.TypedDict):
    pass


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.unspecced.getTaggedSuggestions`."""

    suggestions: t.List['models.AppBskyUnspeccedGetTaggedSuggestions.Suggestion']  #: Suggestions.


class Suggestion(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.getTaggedSuggestions`."""

    subject: string_formats.Uri  #: Subject.
    subject_type: t.Union[t.Literal['actor'], t.Literal['feed'], str]  #: Subject type.
    tag: str  #: Tag.

    py_type: t.Literal['app.bsky.unspecced.getTaggedSuggestions#suggestion'] = Field(
        default='app.bsky.unspecced.getTaggedSuggestions#suggestion', alias='$type', frozen=True
    )
