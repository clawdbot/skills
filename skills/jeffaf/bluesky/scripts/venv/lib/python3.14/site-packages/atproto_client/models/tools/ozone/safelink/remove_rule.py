##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`tools.ozone.safelink.removeRule`."""

    pattern: 'models.ToolsOzoneSafelinkDefs.PatternType'  #: Pattern.
    url: str  #: The URL or domain to remove the rule for.
    comment: t.Optional[str] = None  #: Optional comment about why the rule is being removed.
    created_by: t.Optional[string_formats.Did] = (
        None  #: Optional DID of the user. Only respected when using admin auth.
    )


class DataDict(t.TypedDict):
    pattern: 'models.ToolsOzoneSafelinkDefs.PatternType'  #: Pattern.
    url: str  #: The URL or domain to remove the rule for.
    comment: te.NotRequired[t.Optional[str]]  #: Optional comment about why the rule is being removed.
    created_by: te.NotRequired[
        t.Optional[string_formats.Did]
    ]  #: Optional DID of the user. Only respected when using admin auth.
