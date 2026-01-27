##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client.models.unknown_type import UnknownType
from atproto_client.models import base


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.server.refreshSession`."""

    access_jwt: str  #: Access jwt.
    did: string_formats.Did  #: Did.
    handle: string_formats.Handle  #: Handle.
    refresh_jwt: str  #: Refresh jwt.
    active: t.Optional[bool] = None  #: Active.
    did_doc: t.Optional['UnknownType'] = None  #: Did doc.
    status: t.Optional[t.Union[t.Literal['takendown'], t.Literal['suspended'], t.Literal['deactivated'], str]] = (
        None  #: Hosting status of the account. If not specified, then assume 'active'.
    )
