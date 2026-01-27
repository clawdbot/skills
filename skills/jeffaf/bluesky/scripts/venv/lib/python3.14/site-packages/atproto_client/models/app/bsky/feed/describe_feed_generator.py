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


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.feed.describeFeedGenerator`."""

    did: string_formats.Did  #: Did.
    feeds: t.List['models.AppBskyFeedDescribeFeedGenerator.Feed']  #: Feeds.
    links: t.Optional['models.AppBskyFeedDescribeFeedGenerator.Links'] = None  #: Links.


class Feed(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.describeFeedGenerator`."""

    uri: string_formats.AtUri  #: Uri.

    py_type: t.Literal['app.bsky.feed.describeFeedGenerator#feed'] = Field(
        default='app.bsky.feed.describeFeedGenerator#feed', alias='$type', frozen=True
    )


class Links(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.describeFeedGenerator`."""

    privacy_policy: t.Optional[str] = None  #: Privacy policy.
    terms_of_service: t.Optional[str] = None  #: Terms of service.

    py_type: t.Literal['app.bsky.feed.describeFeedGenerator#links'] = Field(
        default='app.bsky.feed.describeFeedGenerator#links', alias='$type', frozen=True
    )
