##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

if t.TYPE_CHECKING:
    from atproto_client.models.unknown_type import UnknownType
from atproto_client.models import base


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.identity.getRecommendedDidCredentials`."""

    also_known_as: t.Optional[t.List[str]] = None  #: Also known as.
    rotation_keys: t.Optional[t.List[str]] = (
        None  #: Recommended rotation keys for PLC dids. Should be undefined (or ignored) for did:webs.
    )
    services: t.Optional['UnknownType'] = None  #: Services.
    verification_methods: t.Optional['UnknownType'] = None  #: Verification methods.
