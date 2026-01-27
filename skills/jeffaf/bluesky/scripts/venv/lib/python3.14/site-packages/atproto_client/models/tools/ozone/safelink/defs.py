##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Event(base.ModelBase):
    """Definition model for :obj:`tools.ozone.safelink.defs`. An event for URL safety decisions."""

    action: 'models.ToolsOzoneSafelinkDefs.ActionType'  #: Action.
    created_at: string_formats.DateTime  #: Created at.
    created_by: string_formats.Did  #: DID of the user who created this rule.
    event_type: 'models.ToolsOzoneSafelinkDefs.EventType'  #: Event type.
    id: int  #: Auto-incrementing row ID.
    pattern: 'models.ToolsOzoneSafelinkDefs.PatternType'  #: Pattern.
    reason: 'models.ToolsOzoneSafelinkDefs.ReasonType'  #: Reason.
    url: str  #: The URL that this rule applies to.
    comment: t.Optional[str] = None  #: Optional comment about the decision.

    py_type: t.Literal['tools.ozone.safelink.defs#event'] = Field(
        default='tools.ozone.safelink.defs#event', alias='$type', frozen=True
    )


EventType = t.Union[t.Literal['addRule'], t.Literal['updateRule'], t.Literal['removeRule'], str]  #: Event type

PatternType = t.Union[t.Literal['domain'], t.Literal['url'], str]  #: Pattern type

ActionType = t.Union[t.Literal['block'], t.Literal['warn'], t.Literal['whitelist'], str]  #: Action type

ReasonType = t.Union[
    t.Literal['csam'], t.Literal['spam'], t.Literal['phishing'], t.Literal['none'], str
]  #: Reason type


class UrlRule(base.ModelBase):
    """Definition model for :obj:`tools.ozone.safelink.defs`. Input for creating a URL safety rule."""

    action: 'models.ToolsOzoneSafelinkDefs.ActionType'  #: Action.
    created_at: string_formats.DateTime  #: Timestamp when the rule was created.
    created_by: string_formats.Did  #: DID of the user added the rule.
    pattern: 'models.ToolsOzoneSafelinkDefs.PatternType'  #: Pattern.
    reason: 'models.ToolsOzoneSafelinkDefs.ReasonType'  #: Reason.
    updated_at: string_formats.DateTime  #: Timestamp when the rule was last updated.
    url: str  #: The URL or domain to apply the rule to.
    comment: t.Optional[str] = None  #: Optional comment about the decision.

    py_type: t.Literal['tools.ozone.safelink.defs#urlRule'] = Field(
        default='tools.ozone.safelink.defs#urlRule', alias='$type', frozen=True
    )
