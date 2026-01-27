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


class RecordDeleted(base.ModelBase):
    """Definition model for :obj:`app.bsky.notification.defs`."""

    py_type: t.Literal['app.bsky.notification.defs#recordDeleted'] = Field(
        default='app.bsky.notification.defs#recordDeleted', alias='$type', frozen=True
    )


class ChatPreference(base.ModelBase):
    """Definition model for :obj:`app.bsky.notification.defs`."""

    include: t.Union[t.Literal['all'], t.Literal['accepted'], str]  #: Include.
    push: bool  #: Push.

    py_type: t.Literal['app.bsky.notification.defs#chatPreference'] = Field(
        default='app.bsky.notification.defs#chatPreference', alias='$type', frozen=True
    )


class FilterablePreference(base.ModelBase):
    """Definition model for :obj:`app.bsky.notification.defs`."""

    include: t.Union[t.Literal['all'], t.Literal['follows'], str]  #: Include.
    list: bool  #: List.
    push: bool  #: Push.

    py_type: t.Literal['app.bsky.notification.defs#filterablePreference'] = Field(
        default='app.bsky.notification.defs#filterablePreference', alias='$type', frozen=True
    )


class Preference(base.ModelBase):
    """Definition model for :obj:`app.bsky.notification.defs`."""

    list: bool  #: List.
    push: bool  #: Push.

    py_type: t.Literal['app.bsky.notification.defs#preference'] = Field(
        default='app.bsky.notification.defs#preference', alias='$type', frozen=True
    )


class Preferences(base.ModelBase):
    """Definition model for :obj:`app.bsky.notification.defs`."""

    chat: 'models.AppBskyNotificationDefs.ChatPreference'  #: Chat.
    follow: 'models.AppBskyNotificationDefs.FilterablePreference'  #: Follow.
    like: 'models.AppBskyNotificationDefs.FilterablePreference'  #: Like.
    like_via_repost: 'models.AppBskyNotificationDefs.FilterablePreference'  #: Like via repost.
    mention: 'models.AppBskyNotificationDefs.FilterablePreference'  #: Mention.
    quote: 'models.AppBskyNotificationDefs.FilterablePreference'  #: Quote.
    reply: 'models.AppBskyNotificationDefs.FilterablePreference'  #: Reply.
    repost: 'models.AppBskyNotificationDefs.FilterablePreference'  #: Repost.
    repost_via_repost: 'models.AppBskyNotificationDefs.FilterablePreference'  #: Repost via repost.
    starterpack_joined: 'models.AppBskyNotificationDefs.Preference'  #: Starterpack joined.
    subscribed_post: 'models.AppBskyNotificationDefs.Preference'  #: Subscribed post.
    unverified: 'models.AppBskyNotificationDefs.Preference'  #: Unverified.
    verified: 'models.AppBskyNotificationDefs.Preference'  #: Verified.

    py_type: t.Literal['app.bsky.notification.defs#preferences'] = Field(
        default='app.bsky.notification.defs#preferences', alias='$type', frozen=True
    )


class ActivitySubscription(base.ModelBase):
    """Definition model for :obj:`app.bsky.notification.defs`."""

    post: bool  #: Post.
    reply: bool  #: Reply.

    py_type: t.Literal['app.bsky.notification.defs#activitySubscription'] = Field(
        default='app.bsky.notification.defs#activitySubscription', alias='$type', frozen=True
    )


class SubjectActivitySubscription(base.ModelBase):
    """Definition model for :obj:`app.bsky.notification.defs`. Object used to store activity subscription data in stash."""

    activity_subscription: 'models.AppBskyNotificationDefs.ActivitySubscription'  #: Activity subscription.
    subject: string_formats.Did  #: Subject.

    py_type: t.Literal['app.bsky.notification.defs#subjectActivitySubscription'] = Field(
        default='app.bsky.notification.defs#subjectActivitySubscription', alias='$type', frozen=True
    )
