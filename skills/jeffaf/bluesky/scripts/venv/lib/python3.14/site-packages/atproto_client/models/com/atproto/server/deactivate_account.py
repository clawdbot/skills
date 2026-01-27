##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base, string_formats


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.server.deactivateAccount`."""

    delete_after: t.Optional[string_formats.DateTime] = (
        None  #: A recommendation to server as to how long they should hold onto the deactivated account before deleting.
    )


class DataDict(t.TypedDict):
    delete_after: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: A recommendation to server as to how long they should hold onto the deactivated account before deleting.
