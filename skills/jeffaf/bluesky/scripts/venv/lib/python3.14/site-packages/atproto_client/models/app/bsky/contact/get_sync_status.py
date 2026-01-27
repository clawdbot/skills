##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`app.bsky.contact.getSyncStatus`."""


class ParamsDict(t.TypedDict):
    pass


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.contact.getSyncStatus`."""

    sync_status: t.Optional['models.AppBskyContactDefs.SyncStatus'] = (
        None  #: If present, indicates the user has imported their contacts. If not present, indicates the user never used the feature or called `app.bsky.contact.removeData` and didn't import again since.
    )
