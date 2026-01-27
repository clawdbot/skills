##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import base


class SigDetail(base.ModelBase):
    """Definition model for :obj:`tools.ozone.signature.defs`."""

    property: str  #: Property.
    value: str  #: Value.

    py_type: t.Literal['tools.ozone.signature.defs#sigDetail'] = Field(
        default='tools.ozone.signature.defs#sigDetail', alias='$type', frozen=True
    )
