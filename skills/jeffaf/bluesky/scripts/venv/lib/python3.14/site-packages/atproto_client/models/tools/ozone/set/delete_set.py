##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`tools.ozone.set.deleteSet`."""

    name: str  #: Name of the set to delete.


class DataDict(t.TypedDict):
    name: str  #: Name of the set to delete.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.set.deleteSet`."""
