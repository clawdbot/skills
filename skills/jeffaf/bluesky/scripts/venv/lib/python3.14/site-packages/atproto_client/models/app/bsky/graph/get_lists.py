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
    """Parameters model for :obj:`app.bsky.graph.getLists`."""

    actor: string_formats.AtIdentifier  #: The account (actor) to enumerate lists from.
    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    purposes: t.Optional[t.List[t.Union[t.Literal['modlist'], t.Literal['curatelist'], str]]] = (
        None  #: Optional filter by list purpose. If not specified, all supported types are returned.
    )


class ParamsDict(t.TypedDict):
    actor: string_formats.AtIdentifier  #: The account (actor) to enumerate lists from.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    purposes: te.NotRequired[
        t.Optional[t.List[t.Union[t.Literal['modlist'], t.Literal['curatelist'], str]]]
    ]  #: Optional filter by list purpose. If not specified, all supported types are returned.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.graph.getLists`."""

    lists: t.List['models.AppBskyGraphDefs.ListView']  #: Lists.
    cursor: t.Optional[str] = None  #: Cursor.
