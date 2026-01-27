##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`app.bsky.video.getJobStatus`."""

    job_id: str  #: Job id.


class ParamsDict(t.TypedDict):
    job_id: str  #: Job id.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.video.getJobStatus`."""

    job_status: 'models.AppBskyVideoDefs.JobStatus'  #: Job status.
