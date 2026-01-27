##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`tools.ozone.set.deleteValues`."""

    name: str  #: Name of the set to delete values from.
    values: t.List[str] = Field(min_length=1)  #: Array of string values to delete from the set.


class DataDict(t.TypedDict):
    name: str  #: Name of the set to delete values from.
    values: t.List[str]  #: Array of string values to delete from the set.
