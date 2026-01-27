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
    """Input data model for :obj:`tools.ozone.safelink.addRule`."""

    action: 'models.ToolsOzoneSafelinkDefs.ActionType'  #: Action.
    pattern: 'models.ToolsOzoneSafelinkDefs.PatternType'  #: Pattern.
    reason: 'models.ToolsOzoneSafelinkDefs.ReasonType'  #: Reason.
    url: str  #: The URL or domain to apply the rule to.
    comment: t.Optional[str] = None  #: Optional comment about the decision.
    created_by: t.Optional[string_formats.Did] = None  #: Author DID. Only respected when using admin auth.


class DataDict(t.TypedDict):
    action: 'models.ToolsOzoneSafelinkDefs.ActionType'  #: Action.
    pattern: 'models.ToolsOzoneSafelinkDefs.PatternType'  #: Pattern.
    reason: 'models.ToolsOzoneSafelinkDefs.ReasonType'  #: Reason.
    url: str  #: The URL or domain to apply the rule to.
    comment: te.NotRequired[t.Optional[str]]  #: Optional comment about the decision.
    created_by: te.NotRequired[t.Optional[string_formats.Did]]  #: Author DID. Only respected when using admin auth.
