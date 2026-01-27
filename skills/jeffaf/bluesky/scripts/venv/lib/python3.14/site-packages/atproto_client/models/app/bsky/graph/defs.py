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
    from atproto_client.models.unknown_type import UnknownType
from atproto_client.models import base


class ListViewBasic(base.ModelBase):
    """Definition model for :obj:`app.bsky.graph.defs`."""

    cid: string_formats.Cid  #: Cid.
    name: str = Field(min_length=1, max_length=64)  #: Name.
    purpose: 'models.AppBskyGraphDefs.ListPurpose'  #: Purpose.
    uri: string_formats.AtUri  #: Uri.
    avatar: t.Optional[string_formats.Uri] = None  #: Avatar.
    indexed_at: t.Optional[string_formats.DateTime] = None  #: Indexed at.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.
    list_item_count: te.Annotated[t.Optional[int], Field(ge=0)] = None  #: List item count.
    viewer: t.Optional['models.AppBskyGraphDefs.ListViewerState'] = None  #: Viewer.

    py_type: t.Literal['app.bsky.graph.defs#listViewBasic'] = Field(
        default='app.bsky.graph.defs#listViewBasic', alias='$type', frozen=True
    )


class ListView(base.ModelBase):
    """Definition model for :obj:`app.bsky.graph.defs`."""

    cid: string_formats.Cid  #: Cid.
    creator: 'models.AppBskyActorDefs.ProfileView'  #: Creator.
    indexed_at: string_formats.DateTime  #: Indexed at.
    name: str = Field(min_length=1, max_length=64)  #: Name.
    purpose: 'models.AppBskyGraphDefs.ListPurpose'  #: Purpose.
    uri: string_formats.AtUri  #: Uri.
    avatar: t.Optional[string_formats.Uri] = None  #: Avatar.
    description: te.Annotated[t.Optional[str], Field(max_length=3000)] = None  #: Description.
    description_facets: t.Optional[t.List['models.AppBskyRichtextFacet.Main']] = None  #: Description facets.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.
    list_item_count: te.Annotated[t.Optional[int], Field(ge=0)] = None  #: List item count.
    viewer: t.Optional['models.AppBskyGraphDefs.ListViewerState'] = None  #: Viewer.

    py_type: t.Literal['app.bsky.graph.defs#listView'] = Field(
        default='app.bsky.graph.defs#listView', alias='$type', frozen=True
    )


class ListItemView(base.ModelBase):
    """Definition model for :obj:`app.bsky.graph.defs`."""

    subject: 'models.AppBskyActorDefs.ProfileView'  #: Subject.
    uri: string_formats.AtUri  #: Uri.

    py_type: t.Literal['app.bsky.graph.defs#listItemView'] = Field(
        default='app.bsky.graph.defs#listItemView', alias='$type', frozen=True
    )


class StarterPackView(base.ModelBase):
    """Definition model for :obj:`app.bsky.graph.defs`."""

    cid: string_formats.Cid  #: Cid.
    creator: 'models.AppBskyActorDefs.ProfileViewBasic'  #: Creator.
    indexed_at: string_formats.DateTime  #: Indexed at.
    record: 'UnknownType'  #: Record.
    uri: string_formats.AtUri  #: Uri.
    feeds: te.Annotated[t.Optional[t.List['models.AppBskyFeedDefs.GeneratorView']], Field(max_length=3)] = (
        None  #: Feeds.
    )
    joined_all_time_count: te.Annotated[t.Optional[int], Field(ge=0)] = None  #: Joined all time count.
    joined_week_count: te.Annotated[t.Optional[int], Field(ge=0)] = None  #: Joined week count.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.
    list: t.Optional['models.AppBskyGraphDefs.ListViewBasic'] = None  #: List.
    list_items_sample: te.Annotated[
        t.Optional[t.List['models.AppBskyGraphDefs.ListItemView']], Field(max_length=12)
    ] = None  #: List items sample.

    py_type: t.Literal['app.bsky.graph.defs#starterPackView'] = Field(
        default='app.bsky.graph.defs#starterPackView', alias='$type', frozen=True
    )


class StarterPackViewBasic(base.ModelBase):
    """Definition model for :obj:`app.bsky.graph.defs`."""

    cid: string_formats.Cid  #: Cid.
    creator: 'models.AppBskyActorDefs.ProfileViewBasic'  #: Creator.
    indexed_at: string_formats.DateTime  #: Indexed at.
    record: 'UnknownType'  #: Record.
    uri: string_formats.AtUri  #: Uri.
    joined_all_time_count: te.Annotated[t.Optional[int], Field(ge=0)] = None  #: Joined all time count.
    joined_week_count: te.Annotated[t.Optional[int], Field(ge=0)] = None  #: Joined week count.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.
    list_item_count: te.Annotated[t.Optional[int], Field(ge=0)] = None  #: List item count.

    py_type: t.Literal['app.bsky.graph.defs#starterPackViewBasic'] = Field(
        default='app.bsky.graph.defs#starterPackViewBasic', alias='$type', frozen=True
    )


ListPurpose = t.Union[
    'models.AppBskyGraphDefs.Modlist',
    'models.AppBskyGraphDefs.Curatelist',
    'models.AppBskyGraphDefs.Referencelist',
    str,
]  #: List purpose

Modlist = t.Literal[
    'app.bsky.graph.defs#modlist'
]  #: A list of actors to apply an aggregate moderation action (mute/block) on.

Curatelist = t.Literal[
    'app.bsky.graph.defs#curatelist'
]  #: A list of actors used for curation purposes such as list feeds or interaction gating.

Referencelist = t.Literal[
    'app.bsky.graph.defs#referencelist'
]  #: A list of actors used for only for reference purposes such as within a starter pack.


class ListViewerState(base.ModelBase):
    """Definition model for :obj:`app.bsky.graph.defs`."""

    blocked: t.Optional[string_formats.AtUri] = None  #: Blocked.
    muted: t.Optional[bool] = None  #: Muted.

    py_type: t.Literal['app.bsky.graph.defs#listViewerState'] = Field(
        default='app.bsky.graph.defs#listViewerState', alias='$type', frozen=True
    )


class NotFoundActor(base.ModelBase):
    """Definition model for :obj:`app.bsky.graph.defs`. indicates that a handle or DID could not be resolved."""

    actor: string_formats.AtIdentifier  #: Actor.
    not_found: bool = Field(frozen=True)  #: Not found.

    py_type: t.Literal['app.bsky.graph.defs#notFoundActor'] = Field(
        default='app.bsky.graph.defs#notFoundActor', alias='$type', frozen=True
    )


class Relationship(base.ModelBase):
    """Definition model for :obj:`app.bsky.graph.defs`. lists the bi-directional graph relationships between one actor (not indicated in the object), and the target actors (the DID included in the object)."""

    did: string_formats.Did  #: Did.
    blocked_by: t.Optional[string_formats.AtUri] = (
        None  #: If the actor is blocked by this DID, contains the AT-URI of the block record.
    )
    blocked_by_list: t.Optional[string_formats.AtUri] = (
        None  #: If the actor is blocked by this DID via a block list, contains the AT-URI of the listblock record.
    )
    blocking: t.Optional[string_formats.AtUri] = (
        None  #: If the actor blocks this DID, this is the AT-URI of the block record.
    )
    blocking_by_list: t.Optional[string_formats.AtUri] = (
        None  #: If the actor blocks this DID via a block list, this is the AT-URI of the listblock record.
    )
    followed_by: t.Optional[string_formats.AtUri] = (
        None  #: If the actor is followed by this DID, contains the AT-URI of the follow record.
    )
    following: t.Optional[string_formats.AtUri] = (
        None  #: If the actor follows this DID, this is the AT-URI of the follow record.
    )

    py_type: t.Literal['app.bsky.graph.defs#relationship'] = Field(
        default='app.bsky.graph.defs#relationship', alias='$type', frozen=True
    )
