##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import base, string_formats


class Data(base.DataModelBase):
    """Input data model for :obj:`tools.ozone.setting.removeOptions`."""

    keys: t.List[string_formats.Nsid] = Field(min_length=1, max_length=200)  #: Keys.
    scope: t.Union[t.Literal['instance'], t.Literal['personal'], str]  #: Scope.


class DataDict(t.TypedDict):
    keys: t.List[string_formats.Nsid]  #: Keys.
    scope: t.Union[t.Literal['instance'], t.Literal['personal'], str]  #: Scope.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.setting.removeOptions`."""
