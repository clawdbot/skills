##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.video.getUploadLimits`."""

    can_upload: bool  #: Can upload.
    error: t.Optional[str] = None  #: Error.
    message: t.Optional[str] = None  #: Message.
    remaining_daily_bytes: t.Optional[int] = None  #: Remaining daily bytes.
    remaining_daily_videos: t.Optional[int] = None  #: Remaining daily videos.
