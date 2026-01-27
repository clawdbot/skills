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


class PostView(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    author: 'models.AppBskyActorDefs.ProfileViewBasic'  #: Author.
    cid: string_formats.Cid  #: Cid.
    indexed_at: string_formats.DateTime  #: Indexed at.
    record: 'UnknownType'  #: Record.
    uri: string_formats.AtUri  #: Uri.
    bookmark_count: t.Optional[int] = None  #: Bookmark count.
    debug: t.Optional['UnknownType'] = None  #: Debug information for internal development.
    embed: t.Optional[
        te.Annotated[
            t.Union[
                'models.AppBskyEmbedImages.View',
                'models.AppBskyEmbedVideo.View',
                'models.AppBskyEmbedExternal.View',
                'models.AppBskyEmbedRecord.View',
                'models.AppBskyEmbedRecordWithMedia.View',
            ],
            Field(discriminator='py_type'),
        ]
    ] = None  #: Embed.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.
    like_count: t.Optional[int] = None  #: Like count.
    quote_count: t.Optional[int] = None  #: Quote count.
    reply_count: t.Optional[int] = None  #: Reply count.
    repost_count: t.Optional[int] = None  #: Repost count.
    threadgate: t.Optional['models.AppBskyFeedDefs.ThreadgateView'] = None  #: Threadgate.
    viewer: t.Optional['models.AppBskyFeedDefs.ViewerState'] = None  #: Viewer.

    py_type: t.Literal['app.bsky.feed.defs#postView'] = Field(
        default='app.bsky.feed.defs#postView', alias='$type', frozen=True
    )


class ViewerState(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`. Metadata about the requesting account's relationship with the subject content. Only has meaningful content for authed requests."""

    bookmarked: t.Optional[bool] = None  #: Bookmarked.
    embedding_disabled: t.Optional[bool] = None  #: Embedding disabled.
    like: t.Optional[string_formats.AtUri] = None  #: Like.
    pinned: t.Optional[bool] = None  #: Pinned.
    reply_disabled: t.Optional[bool] = None  #: Reply disabled.
    repost: t.Optional[string_formats.AtUri] = None  #: Repost.
    thread_muted: t.Optional[bool] = None  #: Thread muted.

    py_type: t.Literal['app.bsky.feed.defs#viewerState'] = Field(
        default='app.bsky.feed.defs#viewerState', alias='$type', frozen=True
    )


class ThreadContext(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`. Metadata about this post within the context of the thread it is in."""

    root_author_like: t.Optional[string_formats.AtUri] = None  #: Root author like.

    py_type: t.Literal['app.bsky.feed.defs#threadContext'] = Field(
        default='app.bsky.feed.defs#threadContext', alias='$type', frozen=True
    )


class FeedViewPost(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    post: 'models.AppBskyFeedDefs.PostView'  #: Post.
    feed_context: te.Annotated[t.Optional[str], Field(max_length=2000)] = (
        None  #: Context provided by feed generator that may be passed back alongside interactions.
    )
    reason: t.Optional[
        te.Annotated[
            t.Union['models.AppBskyFeedDefs.ReasonRepost', 'models.AppBskyFeedDefs.ReasonPin'],
            Field(discriminator='py_type'),
        ]
    ] = None  #: Reason.
    reply: t.Optional['models.AppBskyFeedDefs.ReplyRef'] = None  #: Reply.
    req_id: te.Annotated[t.Optional[str], Field(max_length=100)] = (
        None  #: Unique identifier per request that may be passed back alongside interactions.
    )

    py_type: t.Literal['app.bsky.feed.defs#feedViewPost'] = Field(
        default='app.bsky.feed.defs#feedViewPost', alias='$type', frozen=True
    )


class ReplyRef(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    parent: te.Annotated[
        t.Union[
            'models.AppBskyFeedDefs.PostView',
            'models.AppBskyFeedDefs.NotFoundPost',
            'models.AppBskyFeedDefs.BlockedPost',
        ],
        Field(discriminator='py_type'),
    ]  #: Parent.
    root: te.Annotated[
        t.Union[
            'models.AppBskyFeedDefs.PostView',
            'models.AppBskyFeedDefs.NotFoundPost',
            'models.AppBskyFeedDefs.BlockedPost',
        ],
        Field(discriminator='py_type'),
    ]  #: Root.
    grandparent_author: t.Optional['models.AppBskyActorDefs.ProfileViewBasic'] = (
        None  #: When parent is a reply to another post, this is the author of that post.
    )

    py_type: t.Literal['app.bsky.feed.defs#replyRef'] = Field(
        default='app.bsky.feed.defs#replyRef', alias='$type', frozen=True
    )


class ReasonRepost(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    by: 'models.AppBskyActorDefs.ProfileViewBasic'  #: By.
    indexed_at: string_formats.DateTime  #: Indexed at.
    cid: t.Optional[string_formats.Cid] = None  #: Cid.
    uri: t.Optional[string_formats.AtUri] = None  #: Uri.

    py_type: t.Literal['app.bsky.feed.defs#reasonRepost'] = Field(
        default='app.bsky.feed.defs#reasonRepost', alias='$type', frozen=True
    )


class ReasonPin(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    py_type: t.Literal['app.bsky.feed.defs#reasonPin'] = Field(
        default='app.bsky.feed.defs#reasonPin', alias='$type', frozen=True
    )


class ThreadViewPost(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    post: 'models.AppBskyFeedDefs.PostView'  #: Post.
    parent: t.Optional[
        te.Annotated[
            t.Union[
                'models.AppBskyFeedDefs.ThreadViewPost',
                'models.AppBskyFeedDefs.NotFoundPost',
                'models.AppBskyFeedDefs.BlockedPost',
            ],
            Field(discriminator='py_type'),
        ]
    ] = None  #: Parent.
    replies: t.Optional[
        t.List[
            te.Annotated[
                t.Union[
                    'models.AppBskyFeedDefs.ThreadViewPost',
                    'models.AppBskyFeedDefs.NotFoundPost',
                    'models.AppBskyFeedDefs.BlockedPost',
                ],
                Field(discriminator='py_type'),
            ]
        ]
    ] = None  #: Replies.
    thread_context: t.Optional['models.AppBskyFeedDefs.ThreadContext'] = None  #: Thread context.

    py_type: t.Literal['app.bsky.feed.defs#threadViewPost'] = Field(
        default='app.bsky.feed.defs#threadViewPost', alias='$type', frozen=True
    )


class NotFoundPost(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    not_found: bool = Field(frozen=True)  #: Not found.
    uri: string_formats.AtUri  #: Uri.

    py_type: t.Literal['app.bsky.feed.defs#notFoundPost'] = Field(
        default='app.bsky.feed.defs#notFoundPost', alias='$type', frozen=True
    )


class BlockedPost(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    author: 'models.AppBskyFeedDefs.BlockedAuthor'  #: Author.
    blocked: bool = Field(frozen=True)  #: Blocked.
    uri: string_formats.AtUri  #: Uri.

    py_type: t.Literal['app.bsky.feed.defs#blockedPost'] = Field(
        default='app.bsky.feed.defs#blockedPost', alias='$type', frozen=True
    )


class BlockedAuthor(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    did: string_formats.Did  #: Did.
    viewer: t.Optional['models.AppBskyActorDefs.ViewerState'] = None  #: Viewer.

    py_type: t.Literal['app.bsky.feed.defs#blockedAuthor'] = Field(
        default='app.bsky.feed.defs#blockedAuthor', alias='$type', frozen=True
    )


class GeneratorView(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    cid: string_formats.Cid  #: Cid.
    creator: 'models.AppBskyActorDefs.ProfileView'  #: Creator.
    did: string_formats.Did  #: Did.
    display_name: str  #: Display name.
    indexed_at: string_formats.DateTime  #: Indexed at.
    uri: string_formats.AtUri  #: Uri.
    accepts_interactions: t.Optional[bool] = None  #: Accepts interactions.
    avatar: t.Optional[string_formats.Uri] = None  #: Avatar.
    content_mode: t.Optional[
        t.Union['models.AppBskyFeedDefs.ContentModeUnspecified', 'models.AppBskyFeedDefs.ContentModeVideo', str]
    ] = None  #: Content mode.
    description: te.Annotated[t.Optional[str], Field(max_length=3000)] = None  #: Description.
    description_facets: t.Optional[t.List['models.AppBskyRichtextFacet.Main']] = None  #: Description facets.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.
    like_count: te.Annotated[t.Optional[int], Field(ge=0)] = None  #: Like count.
    viewer: t.Optional['models.AppBskyFeedDefs.GeneratorViewerState'] = None  #: Viewer.

    py_type: t.Literal['app.bsky.feed.defs#generatorView'] = Field(
        default='app.bsky.feed.defs#generatorView', alias='$type', frozen=True
    )


class GeneratorViewerState(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    like: t.Optional[string_formats.AtUri] = None  #: Like.

    py_type: t.Literal['app.bsky.feed.defs#generatorViewerState'] = Field(
        default='app.bsky.feed.defs#generatorViewerState', alias='$type', frozen=True
    )


class SkeletonFeedPost(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    post: string_formats.AtUri  #: Post.
    feed_context: te.Annotated[t.Optional[str], Field(max_length=2000)] = (
        None  #: Context that will be passed through to client and may be passed to feed generator back alongside interactions.
    )
    reason: t.Optional[
        te.Annotated[
            t.Union['models.AppBskyFeedDefs.SkeletonReasonRepost', 'models.AppBskyFeedDefs.SkeletonReasonPin'],
            Field(discriminator='py_type'),
        ]
    ] = None  #: Reason.

    py_type: t.Literal['app.bsky.feed.defs#skeletonFeedPost'] = Field(
        default='app.bsky.feed.defs#skeletonFeedPost', alias='$type', frozen=True
    )


class SkeletonReasonRepost(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    repost: string_formats.AtUri  #: Repost.

    py_type: t.Literal['app.bsky.feed.defs#skeletonReasonRepost'] = Field(
        default='app.bsky.feed.defs#skeletonReasonRepost', alias='$type', frozen=True
    )


class SkeletonReasonPin(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    py_type: t.Literal['app.bsky.feed.defs#skeletonReasonPin'] = Field(
        default='app.bsky.feed.defs#skeletonReasonPin', alias='$type', frozen=True
    )


class ThreadgateView(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    cid: t.Optional[string_formats.Cid] = None  #: Cid.
    lists: t.Optional[t.List['models.AppBskyGraphDefs.ListViewBasic']] = None  #: Lists.
    record: t.Optional['UnknownType'] = None  #: Record.
    uri: t.Optional[string_formats.AtUri] = None  #: Uri.

    py_type: t.Literal['app.bsky.feed.defs#threadgateView'] = Field(
        default='app.bsky.feed.defs#threadgateView', alias='$type', frozen=True
    )


class Interaction(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.defs`."""

    event: t.Optional[
        t.Union[
            'models.AppBskyFeedDefs.RequestLess',
            'models.AppBskyFeedDefs.RequestMore',
            'models.AppBskyFeedDefs.ClickthroughItem',
            'models.AppBskyFeedDefs.ClickthroughAuthor',
            'models.AppBskyFeedDefs.ClickthroughReposter',
            'models.AppBskyFeedDefs.ClickthroughEmbed',
            'models.AppBskyFeedDefs.InteractionSeen',
            'models.AppBskyFeedDefs.InteractionLike',
            'models.AppBskyFeedDefs.InteractionRepost',
            'models.AppBskyFeedDefs.InteractionReply',
            'models.AppBskyFeedDefs.InteractionQuote',
            'models.AppBskyFeedDefs.InteractionShare',
            str,
        ]
    ] = None  #: Event.
    feed_context: te.Annotated[t.Optional[str], Field(max_length=2000)] = (
        None  #: Context on a feed item that was originally supplied by the feed generator on getFeedSkeleton.
    )
    item: t.Optional[string_formats.AtUri] = None  #: Item.
    req_id: te.Annotated[t.Optional[str], Field(max_length=100)] = (
        None  #: Unique identifier per request that may be passed back alongside interactions.
    )

    py_type: t.Literal['app.bsky.feed.defs#interaction'] = Field(
        default='app.bsky.feed.defs#interaction', alias='$type', frozen=True
    )


RequestLess = t.Literal[
    'app.bsky.feed.defs#requestLess'
]  #: Request that less content like the given feed item be shown in the feed

RequestMore = t.Literal[
    'app.bsky.feed.defs#requestMore'
]  #: Request that more content like the given feed item be shown in the feed

ClickthroughItem = t.Literal['app.bsky.feed.defs#clickthroughItem']  #: User clicked through to the feed item

ClickthroughAuthor = t.Literal[
    'app.bsky.feed.defs#clickthroughAuthor'
]  #: User clicked through to the author of the feed item

ClickthroughReposter = t.Literal[
    'app.bsky.feed.defs#clickthroughReposter'
]  #: User clicked through to the reposter of the feed item

ClickthroughEmbed = t.Literal[
    'app.bsky.feed.defs#clickthroughEmbed'
]  #: User clicked through to the embedded content of the feed item

ContentModeUnspecified = t.Literal[
    'app.bsky.feed.defs#contentModeUnspecified'
]  #: Declares the feed generator returns any types of posts.

ContentModeVideo = t.Literal[
    'app.bsky.feed.defs#contentModeVideo'
]  #: Declares the feed generator returns posts containing app.bsky.embed.video embeds.

InteractionSeen = t.Literal['app.bsky.feed.defs#interactionSeen']  #: Feed item was seen by user

InteractionLike = t.Literal['app.bsky.feed.defs#interactionLike']  #: User liked the feed item

InteractionRepost = t.Literal['app.bsky.feed.defs#interactionRepost']  #: User reposted the feed item

InteractionReply = t.Literal['app.bsky.feed.defs#interactionReply']  #: User replied to the feed item

InteractionQuote = t.Literal['app.bsky.feed.defs#interactionQuote']  #: User quoted the feed item

InteractionShare = t.Literal['app.bsky.feed.defs#interactionShare']  #: User shared the feed item
