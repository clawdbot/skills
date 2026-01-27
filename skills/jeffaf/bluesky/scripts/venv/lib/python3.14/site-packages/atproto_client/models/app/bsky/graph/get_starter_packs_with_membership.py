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
    """Parameters model for :obj:`app.bsky.graph.getStarterPacksWithMembership`."""

    actor: string_formats.AtIdentifier  #: The account (actor) to check for membership.
    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.


class ParamsDict(t.TypedDict):
    actor: string_formats.AtIdentifier  #: The account (actor) to check for membership.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.graph.getStarterPacksWithMembership`."""

    starter_packs_with_membership: t.List[
        'models.AppBskyGraphGetStarterPacksWithMembership.StarterPackWithMembership'
    ]  #: Starter packs with membership.
    cursor: t.Optional[str] = None  #: Cursor.


class StarterPackWithMembership(base.ModelBase):
    """Definition model for :obj:`app.bsky.graph.getStarterPacksWithMembership`. A starter pack and an optional list item indicating membership of a target user to that starter pack."""

    starter_pack: 'models.AppBskyGraphDefs.StarterPackView'  #: Starter pack.
    list_item: t.Optional['models.AppBskyGraphDefs.ListItemView'] = None  #: List item.

    py_type: t.Literal['app.bsky.graph.getStarterPacksWithMembership#starterPackWithMembership'] = Field(
        default='app.bsky.graph.getStarterPacksWithMembership#starterPackWithMembership', alias='$type', frozen=True
    )
