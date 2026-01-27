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
    """Output data model for :obj:`app.bsky.unspecced.getConfig`."""

    check_email_confirmed: t.Optional[bool] = None  #: Check email confirmed.
    live_now: t.Optional[t.List['models.AppBskyUnspeccedGetConfig.LiveNowConfig']] = None  #: Live now.


class LiveNowConfig(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.getConfig`."""

    did: string_formats.Did  #: Did.
    domains: t.List[str]  #: Domains.

    py_type: t.Literal['app.bsky.unspecced.getConfig#liveNowConfig'] = Field(
        default='app.bsky.unspecced.getConfig#liveNowConfig', alias='$type', frozen=True
    )
