##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base

#: Data raw data type.
Data: te.TypeAlias = bytes


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.video.uploadVideo`."""

    job_status: 'models.AppBskyVideoDefs.JobStatus'  #: Job status.
