##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te
from pydantic import Field

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`tools.ozone.verification.revokeVerifications`."""

    uris: t.List[string_formats.AtUri] = Field(
        max_length=100
    )  #: Array of verification record uris to revoke. The AT-URI of the verification record to revoke.
    revoke_reason: te.Annotated[t.Optional[str], Field(max_length=1000)] = (
        None  #: Reason for revoking the verification. This is optional and can be omitted if not needed.
    )


class DataDict(t.TypedDict):
    uris: t.List[
        string_formats.AtUri
    ]  #: Array of verification record uris to revoke. The AT-URI of the verification record to revoke.
    revoke_reason: te.NotRequired[
        t.Optional[str]
    ]  #: Reason for revoking the verification. This is optional and can be omitted if not needed.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.verification.revokeVerifications`."""

    failed_revocations: t.List[
        'models.ToolsOzoneVerificationRevokeVerifications.RevokeError'
    ]  #: List of verification uris that couldn't be revoked, including failure reasons.
    revoked_verifications: t.List[string_formats.AtUri]  #: List of verification uris successfully revoked.


class RevokeError(base.ModelBase):
    """Definition model for :obj:`tools.ozone.verification.revokeVerifications`. Error object for failed revocations."""

    error: str  #: Description of the error that occurred during revocation.
    uri: string_formats.AtUri  #: The AT-URI of the verification record that failed to revoke.

    py_type: t.Literal['tools.ozone.verification.revokeVerifications#revokeError'] = Field(
        default='tools.ozone.verification.revokeVerifications#revokeError', alias='$type', frozen=True
    )
