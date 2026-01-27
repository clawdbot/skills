##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import base, string_formats


class CommitMeta(base.ModelBase):
    """Definition model for :obj:`com.atproto.repo.defs`."""

    cid: string_formats.Cid  #: Cid.
    rev: string_formats.Tid  #: Rev.

    py_type: t.Literal['com.atproto.repo.defs#commitMeta'] = Field(
        default='com.atproto.repo.defs#commitMeta', alias='$type', frozen=True
    )
