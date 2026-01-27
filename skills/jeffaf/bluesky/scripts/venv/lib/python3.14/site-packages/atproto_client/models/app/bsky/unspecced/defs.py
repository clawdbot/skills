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


class SkeletonSearchPost(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`."""

    uri: string_formats.AtUri  #: Uri.

    py_type: t.Literal['app.bsky.unspecced.defs#skeletonSearchPost'] = Field(
        default='app.bsky.unspecced.defs#skeletonSearchPost', alias='$type', frozen=True
    )


class SkeletonSearchActor(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`."""

    did: string_formats.Did  #: Did.

    py_type: t.Literal['app.bsky.unspecced.defs#skeletonSearchActor'] = Field(
        default='app.bsky.unspecced.defs#skeletonSearchActor', alias='$type', frozen=True
    )


class SkeletonSearchStarterPack(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`."""

    uri: string_formats.AtUri  #: Uri.

    py_type: t.Literal['app.bsky.unspecced.defs#skeletonSearchStarterPack'] = Field(
        default='app.bsky.unspecced.defs#skeletonSearchStarterPack', alias='$type', frozen=True
    )


class TrendingTopic(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`."""

    link: str  #: Link.
    topic: str  #: Topic.
    description: t.Optional[str] = None  #: Description.
    display_name: t.Optional[str] = None  #: Display name.

    py_type: t.Literal['app.bsky.unspecced.defs#trendingTopic'] = Field(
        default='app.bsky.unspecced.defs#trendingTopic', alias='$type', frozen=True
    )


class SkeletonTrend(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`."""

    dids: t.List[string_formats.Did]  #: Dids.
    display_name: str  #: Display name.
    link: str  #: Link.
    post_count: int  #: Post count.
    started_at: string_formats.DateTime  #: Started at.
    topic: str  #: Topic.
    category: t.Optional[str] = None  #: Category.
    status: t.Optional[t.Union[t.Literal['hot'], str]] = None  #: Status.

    py_type: t.Literal['app.bsky.unspecced.defs#skeletonTrend'] = Field(
        default='app.bsky.unspecced.defs#skeletonTrend', alias='$type', frozen=True
    )


class TrendView(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`."""

    actors: t.List['models.AppBskyActorDefs.ProfileViewBasic']  #: Actors.
    display_name: str  #: Display name.
    link: str  #: Link.
    post_count: int  #: Post count.
    started_at: string_formats.DateTime  #: Started at.
    topic: str  #: Topic.
    category: t.Optional[str] = None  #: Category.
    status: t.Optional[t.Union[t.Literal['hot'], str]] = None  #: Status.

    py_type: t.Literal['app.bsky.unspecced.defs#trendView'] = Field(
        default='app.bsky.unspecced.defs#trendView', alias='$type', frozen=True
    )


class ThreadItemPost(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`."""

    hidden_by_threadgate: bool  #: The threadgate created by the author indicates this post as a reply to be hidden for everyone consuming the thread.
    more_parents: bool  #: This post has more parents that were not present in the response. This is just a boolean, without the number of parents.
    more_replies: int  #: This post has more replies that were not present in the response. This is a numeric value, which is best-effort and might not be accurate.
    muted_by_viewer: bool  #: This is by an account muted by the viewer requesting it.
    op_thread: bool  #: This post is part of a contiguous thread by the OP from the thread root. Many different OP threads can happen in the same thread.
    post: 'models.AppBskyFeedDefs.PostView'  #: Post.

    py_type: t.Literal['app.bsky.unspecced.defs#threadItemPost'] = Field(
        default='app.bsky.unspecced.defs#threadItemPost', alias='$type', frozen=True
    )


class ThreadItemNoUnauthenticated(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`."""

    py_type: t.Literal['app.bsky.unspecced.defs#threadItemNoUnauthenticated'] = Field(
        default='app.bsky.unspecced.defs#threadItemNoUnauthenticated', alias='$type', frozen=True
    )


class ThreadItemNotFound(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`."""

    py_type: t.Literal['app.bsky.unspecced.defs#threadItemNotFound'] = Field(
        default='app.bsky.unspecced.defs#threadItemNotFound', alias='$type', frozen=True
    )


class ThreadItemBlocked(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`."""

    author: 'models.AppBskyFeedDefs.BlockedAuthor'  #: Author.

    py_type: t.Literal['app.bsky.unspecced.defs#threadItemBlocked'] = Field(
        default='app.bsky.unspecced.defs#threadItemBlocked', alias='$type', frozen=True
    )


class AgeAssuranceState(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`. The computed state of the age assurance process, returned to the user in question on certain authenticated requests."""

    status: t.Union[
        t.Literal['unknown'], t.Literal['pending'], t.Literal['assured'], t.Literal['blocked'], str
    ]  #: The status of the age assurance process.
    last_initiated_at: t.Optional[string_formats.DateTime] = None  #: The timestamp when this state was last updated.

    py_type: t.Literal['app.bsky.unspecced.defs#ageAssuranceState'] = Field(
        default='app.bsky.unspecced.defs#ageAssuranceState', alias='$type', frozen=True
    )


class AgeAssuranceEvent(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.defs`. Object used to store age assurance data in stash."""

    attempt_id: str  #: The unique identifier for this instance of the age assurance flow, in UUID format.
    created_at: string_formats.DateTime  #: The date and time of this write operation.
    status: t.Union[
        t.Literal['unknown'], t.Literal['pending'], t.Literal['assured'], str
    ]  #: The status of the age assurance process.
    complete_ip: t.Optional[str] = None  #: The IP address used when completing the AA flow.
    complete_ua: t.Optional[str] = None  #: The user agent used when completing the AA flow.
    email: t.Optional[str] = None  #: The email used for AA.
    init_ip: t.Optional[str] = None  #: The IP address used when initiating the AA flow.
    init_ua: t.Optional[str] = None  #: The user agent used when initiating the AA flow.

    py_type: t.Literal['app.bsky.unspecced.defs#ageAssuranceEvent'] = Field(
        default='app.bsky.unspecced.defs#ageAssuranceEvent', alias='$type', frozen=True
    )
