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


class Data(base.DataModelBase):
    """Input data model for :obj:`tools.ozone.verification.grantVerifications`."""

    verifications: t.List['models.ToolsOzoneVerificationGrantVerifications.VerificationInput'] = Field(
        max_length=100
    )  #: Array of verification requests to process.


class DataDict(t.TypedDict):
    verifications: t.List[
        'models.ToolsOzoneVerificationGrantVerifications.VerificationInput'
    ]  #: Array of verification requests to process.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.verification.grantVerifications`."""

    failed_verifications: t.List['models.ToolsOzoneVerificationGrantVerifications.GrantError']  #: Failed verifications.
    verifications: t.List['models.ToolsOzoneVerificationDefs.VerificationView']  #: Verifications.


class VerificationInput(base.ModelBase):
    """Definition model for :obj:`tools.ozone.verification.grantVerifications`."""

    display_name: str  #: Display name of the subject the verification applies to at the moment of verifying.
    handle: string_formats.Handle  #: Handle of the subject the verification applies to at the moment of verifying.
    subject: string_formats.Did  #: The did of the subject being verified.
    created_at: t.Optional[string_formats.DateTime] = (
        None  #: Timestamp for verification record. Defaults to current time when not specified.
    )

    py_type: t.Literal['tools.ozone.verification.grantVerifications#verificationInput'] = Field(
        default='tools.ozone.verification.grantVerifications#verificationInput', alias='$type', frozen=True
    )


class GrantError(base.ModelBase):
    """Definition model for :obj:`tools.ozone.verification.grantVerifications`. Error object for failed verifications."""

    error: str  #: Error message describing the reason for failure.
    subject: string_formats.Did  #: The did of the subject being verified.

    py_type: t.Literal['tools.ozone.verification.grantVerifications#grantError'] = Field(
        default='tools.ozone.verification.grantVerifications#grantError', alias='$type', frozen=True
    )
