##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base, string_formats


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`tools.ozone.moderation.getRecord`."""

    uri: string_formats.AtUri  #: Uri.
    cid: t.Optional[string_formats.Cid] = None  #: Cid.


class ParamsDict(t.TypedDict):
    uri: string_formats.AtUri  #: Uri.
    cid: te.NotRequired[t.Optional[string_formats.Cid]]  #: Cid.
