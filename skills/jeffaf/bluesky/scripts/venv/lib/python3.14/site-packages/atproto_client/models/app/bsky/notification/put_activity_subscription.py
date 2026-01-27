##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`app.bsky.notification.putActivitySubscription`."""

    activity_subscription: 'models.AppBskyNotificationDefs.ActivitySubscription'  #: Activity subscription.
    subject: string_formats.Did  #: Subject.


class DataDict(t.TypedDict):
    activity_subscription: 'models.AppBskyNotificationDefs.ActivitySubscription'  #: Activity subscription.
    subject: string_formats.Did  #: Subject.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.notification.putActivitySubscription`."""

    subject: string_formats.Did  #: Subject.
    activity_subscription: t.Optional['models.AppBskyNotificationDefs.ActivitySubscription'] = (
        None  #: Activity subscription.
    )
