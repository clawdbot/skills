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
    """Parameters model for :obj:`app.bsky.graph.getListsWithMembership`."""

    actor: string_formats.AtIdentifier  #: The account (actor) to check for membership.
    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    purposes: t.Optional[t.List[t.Union[t.Literal['modlist'], t.Literal['curatelist'], str]]] = (
        None  #: Optional filter by list purpose. If not specified, all supported types are returned.
    )


class ParamsDict(t.TypedDict):
    actor: string_formats.AtIdentifier  #: The account (actor) to check for membership.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    purposes: te.NotRequired[
        t.Optional[t.List[t.Union[t.Literal['modlist'], t.Literal['curatelist'], str]]]
    ]  #: Optional filter by list purpose. If not specified, all supported types are returned.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.graph.getListsWithMembership`."""

    lists_with_membership: t.List[
        'models.AppBskyGraphGetListsWithMembership.ListWithMembership'
    ]  #: Lists with membership.
    cursor: t.Optional[str] = None  #: Cursor.


class ListWithMembership(base.ModelBase):
    """Definition model for :obj:`app.bsky.graph.getListsWithMembership`. A list and an optional list item indicating membership of a target user to that list."""

    list: 'models.AppBskyGraphDefs.ListView'  #: List.
    list_item: t.Optional['models.AppBskyGraphDefs.ListItemView'] = None  #: List item.

    py_type: t.Literal['app.bsky.graph.getListsWithMembership#listWithMembership'] = Field(
        default='app.bsky.graph.getListsWithMembership#listWithMembership', alias='$type', frozen=True
    )
