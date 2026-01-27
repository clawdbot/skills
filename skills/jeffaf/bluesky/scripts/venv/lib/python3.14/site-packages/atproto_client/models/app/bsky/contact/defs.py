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


class MatchAndContactIndex(base.ModelBase):
    """Definition model for :obj:`app.bsky.contact.defs`. Associates a profile with the positional index of the contact import input in the call to `app.bsky.contact.importContacts`, so clients can know which phone caused a particular match."""

    contact_index: int = Field(ge=0, le=999)  #: The index of this match in the import contact input.
    match: 'models.AppBskyActorDefs.ProfileView'  #: Profile of the matched user.

    py_type: t.Literal['app.bsky.contact.defs#matchAndContactIndex'] = Field(
        default='app.bsky.contact.defs#matchAndContactIndex', alias='$type', frozen=True
    )


class SyncStatus(base.ModelBase):
    """Definition model for :obj:`app.bsky.contact.defs`."""

    matches_count: int = Field(
        ge=0
    )  #: Number of existing contact matches resulting of the user imports and of their imported contacts having imported the user. Matches stop being counted when the user either follows the matched contact or dismisses the match.
    synced_at: string_formats.DateTime  #: Last date when contacts where imported.

    py_type: t.Literal['app.bsky.contact.defs#syncStatus'] = Field(
        default='app.bsky.contact.defs#syncStatus', alias='$type', frozen=True
    )
