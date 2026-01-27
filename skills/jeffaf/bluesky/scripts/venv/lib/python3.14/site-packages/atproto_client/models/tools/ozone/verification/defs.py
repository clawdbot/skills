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


class VerificationView(base.ModelBase):
    """Definition model for :obj:`tools.ozone.verification.defs`. Verification data for the associated subject."""

    created_at: string_formats.DateTime  #: Timestamp when the verification was created.
    display_name: str  #: Display name of the subject the verification applies to at the moment of verifying, which might not be the same at the time of viewing. The verification is only valid if the current displayName matches the one at the time of verifying.
    handle: string_formats.Handle  #: Handle of the subject the verification applies to at the moment of verifying, which might not be the same at the time of viewing. The verification is only valid if the current handle matches the one at the time of verifying.
    issuer: string_formats.Did  #: The user who issued this verification.
    subject: string_formats.Did  #: The subject of the verification.
    uri: string_formats.AtUri  #: The AT-URI of the verification record.
    issuer_profile: t.Optional[te.Annotated[t.Union['base.UnknownUnionModel'], Field()]] = None  #: Issuer profile.
    issuer_repo: t.Optional[
        te.Annotated[
            t.Union[
                'models.ToolsOzoneModerationDefs.RepoViewDetail', 'models.ToolsOzoneModerationDefs.RepoViewNotFound'
            ],
            Field(discriminator='py_type'),
        ]
    ] = None  #: Issuer repo.
    revoke_reason: t.Optional[str] = (
        None  #: Describes the reason for revocation, also indicating that the verification is no longer valid.
    )
    revoked_at: t.Optional[string_formats.DateTime] = None  #: Timestamp when the verification was revoked.
    revoked_by: t.Optional[string_formats.Did] = None  #: The user who revoked this verification.
    subject_profile: t.Optional[te.Annotated[t.Union['base.UnknownUnionModel'], Field()]] = None  #: Subject profile.
    subject_repo: t.Optional[
        te.Annotated[
            t.Union[
                'models.ToolsOzoneModerationDefs.RepoViewDetail', 'models.ToolsOzoneModerationDefs.RepoViewNotFound'
            ],
            Field(discriminator='py_type'),
        ]
    ] = None  #: Subject repo.

    py_type: t.Literal['tools.ozone.verification.defs#verificationView'] = Field(
        default='tools.ozone.verification.defs#verificationView', alias='$type', frozen=True
    )
