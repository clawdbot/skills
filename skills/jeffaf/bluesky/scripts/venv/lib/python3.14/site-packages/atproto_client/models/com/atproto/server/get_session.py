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
    """Output data model for :obj:`com.atproto.server.getSession`."""

    did: string_formats.Did  #: Did.
    handle: string_formats.Handle  #: Handle.
    active: t.Optional[bool] = None  #: Active.
    did_doc: t.Optional['UnknownType'] = None  #: Did doc.
    email: t.Optional[str] = None  #: Email.
    email_auth_factor: t.Optional[bool] = None  #: Email auth factor.
    email_confirmed: t.Optional[bool] = None  #: Email confirmed.
    status: t.Optional[t.Union[t.Literal['takendown'], t.Literal['suspended'], t.Literal['deactivated'], str]] = (
        None  #: If active=false, this optional field indicates a possible reason for why the account is not active. If active=false and no status is supplied, then the host makes no claim for why the repository is no longer being hosted.
    )
