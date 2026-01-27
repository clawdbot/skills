##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client.models.unknown_type import UnknownType
from atproto_client.models import base


class IdentityInfo(base.ModelBase):
    """Definition model for :obj:`com.atproto.identity.defs`."""

    did: string_formats.Did  #: Did.
    did_doc: 'UnknownType'  #: The complete DID document for the identity.
    handle: string_formats.Handle  #: The validated handle of the account; or 'handle.invalid' if the handle did not bi-directionally match the DID document.

    py_type: t.Literal['com.atproto.identity.defs#identityInfo'] = Field(
        default='com.atproto.identity.defs#identityInfo', alias='$type', frozen=True
    )
