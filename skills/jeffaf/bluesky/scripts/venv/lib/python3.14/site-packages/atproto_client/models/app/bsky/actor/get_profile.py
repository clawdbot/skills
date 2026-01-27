##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base, string_formats


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`app.bsky.actor.getProfile`."""

    actor: string_formats.AtIdentifier  #: Handle or DID of account to fetch profile of.


class ParamsDict(t.TypedDict):
    actor: string_formats.AtIdentifier  #: Handle or DID of account to fetch profile of.
