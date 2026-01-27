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
    """Input data model for :obj:`tools.ozone.moderation.cancelScheduledActions`."""

    subjects: t.List[string_formats.Did] = Field(
        max_length=100
    )  #: Array of DID subjects to cancel scheduled actions for.
    comment: t.Optional[str] = None  #: Optional comment describing the reason for cancellation.


class DataDict(t.TypedDict):
    subjects: t.List[string_formats.Did]  #: Array of DID subjects to cancel scheduled actions for.
    comment: te.NotRequired[t.Optional[str]]  #: Optional comment describing the reason for cancellation.


class CancellationResults(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.cancelScheduledActions`."""

    failed: t.List[
        'models.ToolsOzoneModerationCancelScheduledActions.FailedCancellation'
    ]  #: DIDs for which cancellation failed with error details.
    succeeded: t.List[string_formats.Did]  #: DIDs for which all pending scheduled actions were successfully cancelled.

    py_type: t.Literal['tools.ozone.moderation.cancelScheduledActions#cancellationResults'] = Field(
        default='tools.ozone.moderation.cancelScheduledActions#cancellationResults', alias='$type', frozen=True
    )


class FailedCancellation(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.cancelScheduledActions`."""

    did: string_formats.Did  #: Did.
    error: str  #: Error.
    error_code: t.Optional[str] = None  #: Error code.

    py_type: t.Literal['tools.ozone.moderation.cancelScheduledActions#failedCancellation'] = Field(
        default='tools.ozone.moderation.cancelScheduledActions#failedCancellation', alias='$type', frozen=True
    )
