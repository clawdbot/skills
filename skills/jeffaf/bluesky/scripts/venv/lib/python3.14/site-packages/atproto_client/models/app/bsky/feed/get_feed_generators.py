##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`app.bsky.feed.getFeedGenerators`."""

    feeds: t.List[string_formats.AtUri]  #: Feeds.


class ParamsDict(t.TypedDict):
    feeds: t.List[string_formats.AtUri]  #: Feeds.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.feed.getFeedGenerators`."""

    feeds: t.List['models.AppBskyFeedDefs.GeneratorView']  #: Feeds.
