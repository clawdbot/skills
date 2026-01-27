##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te
from pydantic import Field

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base

Access = t.Union[
    t.Literal['unknown'], t.Literal['none'], t.Literal['safe'], t.Literal['full'], str
]  #: The access level granted based on Age Assurance data we've processed.

Status = t.Union[
    t.Literal['unknown'], t.Literal['pending'], t.Literal['assured'], t.Literal['blocked'], str
]  #: The status of the Age Assurance process.


class State(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`. The user's computed Age Assurance state."""

    access: 'models.AppBskyAgeassuranceDefs.Access'  #: Access.
    status: 'models.AppBskyAgeassuranceDefs.Status'  #: Status.
    last_initiated_at: t.Optional[string_formats.DateTime] = None  #: The timestamp when this state was last updated.

    py_type: t.Literal['app.bsky.ageassurance.defs#state'] = Field(
        default='app.bsky.ageassurance.defs#state', alias='$type', frozen=True
    )


class StateMetadata(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`. Additional metadata needed to compute Age Assurance state client-side."""

    account_created_at: t.Optional[string_formats.DateTime] = None  #: The account creation timestamp.

    py_type: t.Literal['app.bsky.ageassurance.defs#stateMetadata'] = Field(
        default='app.bsky.ageassurance.defs#stateMetadata', alias='$type', frozen=True
    )


class Config(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`."""

    regions: t.List['models.AppBskyAgeassuranceDefs.ConfigRegion']  #: The per-region Age Assurance configuration.

    py_type: t.Literal['app.bsky.ageassurance.defs#config'] = Field(
        default='app.bsky.ageassurance.defs#config', alias='$type', frozen=True
    )


class ConfigRegion(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`. The Age Assurance configuration for a specific region."""

    country_code: str  #: The ISO 3166-1 alpha-2 country code this configuration applies to.
    rules: t.List[
        te.Annotated[
            t.Union[
                'models.AppBskyAgeassuranceDefs.ConfigRegionRuleDefault',
                'models.AppBskyAgeassuranceDefs.ConfigRegionRuleIfDeclaredOverAge',
                'models.AppBskyAgeassuranceDefs.ConfigRegionRuleIfDeclaredUnderAge',
                'models.AppBskyAgeassuranceDefs.ConfigRegionRuleIfAssuredOverAge',
                'models.AppBskyAgeassuranceDefs.ConfigRegionRuleIfAssuredUnderAge',
                'models.AppBskyAgeassuranceDefs.ConfigRegionRuleIfAccountNewerThan',
                'models.AppBskyAgeassuranceDefs.ConfigRegionRuleIfAccountOlderThan',
            ],
            Field(discriminator='py_type'),
        ]
    ]  #: The ordered list of Age Assurance rules that apply to this region. Rules should be applied in order, and the first matching rule determines the access level granted. The rules array should always include a default rule as the last item.
    region_code: t.Optional[str] = (
        None  #: The ISO 3166-2 region code this configuration applies to. If omitted, the configuration applies to the entire country.
    )

    py_type: t.Literal['app.bsky.ageassurance.defs#configRegion'] = Field(
        default='app.bsky.ageassurance.defs#configRegion', alias='$type', frozen=True
    )


class ConfigRegionRuleDefault(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`. Age Assurance rule that applies by default."""

    access: 'models.AppBskyAgeassuranceDefs.Access'  #: Access.

    py_type: t.Literal['app.bsky.ageassurance.defs#configRegionRuleDefault'] = Field(
        default='app.bsky.ageassurance.defs#configRegionRuleDefault', alias='$type', frozen=True
    )


class ConfigRegionRuleIfDeclaredOverAge(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`. Age Assurance rule that applies if the user has declared themselves equal-to or over a certain age."""

    access: 'models.AppBskyAgeassuranceDefs.Access'  #: Access.
    age: int  #: The age threshold as a whole integer.

    py_type: t.Literal['app.bsky.ageassurance.defs#configRegionRuleIfDeclaredOverAge'] = Field(
        default='app.bsky.ageassurance.defs#configRegionRuleIfDeclaredOverAge', alias='$type', frozen=True
    )


class ConfigRegionRuleIfDeclaredUnderAge(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`. Age Assurance rule that applies if the user has declared themselves under a certain age."""

    access: 'models.AppBskyAgeassuranceDefs.Access'  #: Access.
    age: int  #: The age threshold as a whole integer.

    py_type: t.Literal['app.bsky.ageassurance.defs#configRegionRuleIfDeclaredUnderAge'] = Field(
        default='app.bsky.ageassurance.defs#configRegionRuleIfDeclaredUnderAge', alias='$type', frozen=True
    )


class ConfigRegionRuleIfAssuredOverAge(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`. Age Assurance rule that applies if the user has been assured to be equal-to or over a certain age."""

    access: 'models.AppBskyAgeassuranceDefs.Access'  #: Access.
    age: int  #: The age threshold as a whole integer.

    py_type: t.Literal['app.bsky.ageassurance.defs#configRegionRuleIfAssuredOverAge'] = Field(
        default='app.bsky.ageassurance.defs#configRegionRuleIfAssuredOverAge', alias='$type', frozen=True
    )


class ConfigRegionRuleIfAssuredUnderAge(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`. Age Assurance rule that applies if the user has been assured to be under a certain age."""

    access: 'models.AppBskyAgeassuranceDefs.Access'  #: Access.
    age: int  #: The age threshold as a whole integer.

    py_type: t.Literal['app.bsky.ageassurance.defs#configRegionRuleIfAssuredUnderAge'] = Field(
        default='app.bsky.ageassurance.defs#configRegionRuleIfAssuredUnderAge', alias='$type', frozen=True
    )


class ConfigRegionRuleIfAccountNewerThan(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`. Age Assurance rule that applies if the account is equal-to or newer than a certain date."""

    access: 'models.AppBskyAgeassuranceDefs.Access'  #: Access.
    date: string_formats.DateTime  #: The date threshold as a datetime string.

    py_type: t.Literal['app.bsky.ageassurance.defs#configRegionRuleIfAccountNewerThan'] = Field(
        default='app.bsky.ageassurance.defs#configRegionRuleIfAccountNewerThan', alias='$type', frozen=True
    )


class ConfigRegionRuleIfAccountOlderThan(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`. Age Assurance rule that applies if the account is older than a certain date."""

    access: 'models.AppBskyAgeassuranceDefs.Access'  #: Access.
    date: string_formats.DateTime  #: The date threshold as a datetime string.

    py_type: t.Literal['app.bsky.ageassurance.defs#configRegionRuleIfAccountOlderThan'] = Field(
        default='app.bsky.ageassurance.defs#configRegionRuleIfAccountOlderThan', alias='$type', frozen=True
    )


class Event(base.ModelBase):
    """Definition model for :obj:`app.bsky.ageassurance.defs`. Object used to store Age Assurance data in stash."""

    access: t.Union[
        t.Literal['unknown'], t.Literal['none'], t.Literal['safe'], t.Literal['full'], str
    ]  #: The access level granted based on Age Assurance data we've processed.
    attempt_id: str  #: The unique identifier for this instance of the Age Assurance flow, in UUID format.
    country_code: str  #: The ISO 3166-1 alpha-2 country code provided when beginning the Age Assurance flow.
    created_at: string_formats.DateTime  #: The date and time of this write operation.
    status: t.Union[
        t.Literal['unknown'], t.Literal['pending'], t.Literal['assured'], t.Literal['blocked'], str
    ]  #: The status of the Age Assurance process.
    complete_ip: t.Optional[str] = None  #: The IP address used when completing the Age Assurance flow.
    complete_ua: t.Optional[str] = None  #: The user agent used when completing the Age Assurance flow.
    email: t.Optional[str] = None  #: The email used for Age Assurance.
    init_ip: t.Optional[str] = None  #: The IP address used when initiating the Age Assurance flow.
    init_ua: t.Optional[str] = None  #: The user agent used when initiating the Age Assurance flow.
    region_code: t.Optional[str] = None  #: The ISO 3166-2 region code provided when beginning the Age Assurance flow.

    py_type: t.Literal['app.bsky.ageassurance.defs#event'] = Field(
        default='app.bsky.ageassurance.defs#event', alias='$type', frozen=True
    )
