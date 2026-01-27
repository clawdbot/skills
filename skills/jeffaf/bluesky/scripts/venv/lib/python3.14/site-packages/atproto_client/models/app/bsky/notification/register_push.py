##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base, string_formats


class Data(base.DataModelBase):
    """Input data model for :obj:`app.bsky.notification.registerPush`."""

    app_id: str  #: App id.
    platform: t.Union[t.Literal['ios'], t.Literal['android'], t.Literal['web'], str]  #: Platform.
    service_did: string_formats.Did  #: Service did.
    token: str  #: Token.
    age_restricted: t.Optional[bool] = None  #: Set to true when the actor is age restricted.


class DataDict(t.TypedDict):
    app_id: str  #: App id.
    platform: t.Union[t.Literal['ios'], t.Literal['android'], t.Literal['web'], str]  #: Platform.
    service_did: string_formats.Did  #: Service did.
    token: str  #: Token.
    age_restricted: te.NotRequired[t.Optional[bool]]  #: Set to true when the actor is age restricted.
