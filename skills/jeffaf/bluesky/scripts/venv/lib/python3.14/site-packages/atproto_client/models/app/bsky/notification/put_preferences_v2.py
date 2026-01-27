##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`app.bsky.notification.putPreferencesV2`."""

    chat: t.Optional['models.AppBskyNotificationDefs.ChatPreference'] = None  #: Chat.
    follow: t.Optional['models.AppBskyNotificationDefs.FilterablePreference'] = None  #: Follow.
    like: t.Optional['models.AppBskyNotificationDefs.FilterablePreference'] = None  #: Like.
    like_via_repost: t.Optional['models.AppBskyNotificationDefs.FilterablePreference'] = None  #: Like via repost.
    mention: t.Optional['models.AppBskyNotificationDefs.FilterablePreference'] = None  #: Mention.
    quote: t.Optional['models.AppBskyNotificationDefs.FilterablePreference'] = None  #: Quote.
    reply: t.Optional['models.AppBskyNotificationDefs.FilterablePreference'] = None  #: Reply.
    repost: t.Optional['models.AppBskyNotificationDefs.FilterablePreference'] = None  #: Repost.
    repost_via_repost: t.Optional['models.AppBskyNotificationDefs.FilterablePreference'] = None  #: Repost via repost.
    starterpack_joined: t.Optional['models.AppBskyNotificationDefs.Preference'] = None  #: Starterpack joined.
    subscribed_post: t.Optional['models.AppBskyNotificationDefs.Preference'] = None  #: Subscribed post.
    unverified: t.Optional['models.AppBskyNotificationDefs.Preference'] = None  #: Unverified.
    verified: t.Optional['models.AppBskyNotificationDefs.Preference'] = None  #: Verified.


class DataDict(t.TypedDict):
    chat: te.NotRequired[t.Optional['models.AppBskyNotificationDefs.ChatPreference']]  #: Chat.
    follow: te.NotRequired[t.Optional['models.AppBskyNotificationDefs.FilterablePreference']]  #: Follow.
    like: te.NotRequired[t.Optional['models.AppBskyNotificationDefs.FilterablePreference']]  #: Like.
    like_via_repost: te.NotRequired[
        t.Optional['models.AppBskyNotificationDefs.FilterablePreference']
    ]  #: Like via repost.
    mention: te.NotRequired[t.Optional['models.AppBskyNotificationDefs.FilterablePreference']]  #: Mention.
    quote: te.NotRequired[t.Optional['models.AppBskyNotificationDefs.FilterablePreference']]  #: Quote.
    reply: te.NotRequired[t.Optional['models.AppBskyNotificationDefs.FilterablePreference']]  #: Reply.
    repost: te.NotRequired[t.Optional['models.AppBskyNotificationDefs.FilterablePreference']]  #: Repost.
    repost_via_repost: te.NotRequired[
        t.Optional['models.AppBskyNotificationDefs.FilterablePreference']
    ]  #: Repost via repost.
    starterpack_joined: te.NotRequired[t.Optional['models.AppBskyNotificationDefs.Preference']]  #: Starterpack joined.
    subscribed_post: te.NotRequired[t.Optional['models.AppBskyNotificationDefs.Preference']]  #: Subscribed post.
    unverified: te.NotRequired[t.Optional['models.AppBskyNotificationDefs.Preference']]  #: Unverified.
    verified: te.NotRequired[t.Optional['models.AppBskyNotificationDefs.Preference']]  #: Verified.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.notification.putPreferencesV2`."""

    preferences: 'models.AppBskyNotificationDefs.Preferences'  #: Preferences.
