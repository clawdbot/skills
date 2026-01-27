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


class Label(base.ModelBase):
    """Definition model for :obj:`com.atproto.label.defs`. Metadata tag on an atproto resource (eg, repo or record)."""

    cts: string_formats.DateTime  #: Timestamp when this label was created.
    src: string_formats.Did  #: DID of the actor who created this label.
    uri: (
        string_formats.Uri
    )  #: AT URI of the record, repository (account), or other resource that this label applies to.
    val: str = Field(max_length=128)  #: The short string name of the value or type of this label.
    cid: t.Optional[string_formats.Cid] = (
        None  #: Optionally, CID specifying the specific version of 'uri' resource this label applies to.
    )
    exp: t.Optional[string_formats.DateTime] = None  #: Timestamp at which this label expires (no longer applies).
    neg: t.Optional[bool] = None  #: If true, this is a negation label, overwriting a previous label.
    sig: t.Optional[t.Union[str, bytes]] = None  #: Signature of dag-cbor encoded label.
    ver: t.Optional[int] = None  #: The AT Protocol version of the label object.

    py_type: t.Literal['com.atproto.label.defs#label'] = Field(
        default='com.atproto.label.defs#label', alias='$type', frozen=True
    )


class SelfLabels(base.ModelBase):
    """Definition model for :obj:`com.atproto.label.defs`. Metadata tags on an atproto record, published by the author within the record."""

    values: t.List['models.ComAtprotoLabelDefs.SelfLabel'] = Field(max_length=10)  #: Values.

    py_type: t.Literal['com.atproto.label.defs#selfLabels'] = Field(
        default='com.atproto.label.defs#selfLabels', alias='$type', frozen=True
    )


class SelfLabel(base.ModelBase):
    """Definition model for :obj:`com.atproto.label.defs`. Metadata tag on an atproto record, published by the author within the record. Note that schemas should use #selfLabels, not #selfLabel."""

    val: str = Field(max_length=128)  #: The short string name of the value or type of this label.

    py_type: t.Literal['com.atproto.label.defs#selfLabel'] = Field(
        default='com.atproto.label.defs#selfLabel', alias='$type', frozen=True
    )


class LabelValueDefinition(base.ModelBase):
    """Definition model for :obj:`com.atproto.label.defs`. Declares a label value and its expected interpretations and behaviors."""

    blurs: t.Union[
        t.Literal['content'], t.Literal['media'], t.Literal['none'], str
    ]  #: What should this label hide in the UI, if applied? 'content' hides all of the target; 'media' hides the images/video/audio; 'none' hides nothing.
    identifier: str = Field(
        max_length=100
    )  #: The value of the label being defined. Must only include lowercase ascii and the '-' character ([a-z-]+).
    locales: t.List['models.ComAtprotoLabelDefs.LabelValueDefinitionStrings']  #: Locales.
    severity: t.Union[
        t.Literal['inform'], t.Literal['alert'], t.Literal['none'], str
    ]  #: How should a client visually convey this label? 'inform' means neutral and informational; 'alert' means negative and warning; 'none' means show nothing.
    adult_only: t.Optional[bool] = (
        None  #: Does the user need to have adult content enabled in order to configure this label?
    )
    default_setting: t.Optional[t.Union[t.Literal['ignore'], t.Literal['warn'], t.Literal['hide'], str]] = (
        'warn'  #: The default setting for this label.
    )

    py_type: t.Literal['com.atproto.label.defs#labelValueDefinition'] = Field(
        default='com.atproto.label.defs#labelValueDefinition', alias='$type', frozen=True
    )


class LabelValueDefinitionStrings(base.ModelBase):
    """Definition model for :obj:`com.atproto.label.defs`. Strings which describe the label in the UI, localized into a specific language."""

    description: str = Field(
        max_length=100000
    )  #: A longer description of what the label means and why it might be applied.
    lang: string_formats.Language  #: The code of the language these strings are written in.
    name: str = Field(max_length=640)  #: A short human-readable name for the label.

    py_type: t.Literal['com.atproto.label.defs#labelValueDefinitionStrings'] = Field(
        default='com.atproto.label.defs#labelValueDefinitionStrings', alias='$type', frozen=True
    )


LabelValue = t.Union[
    t.Literal['!hide'],
    t.Literal['!no-promote'],
    t.Literal['!warn'],
    t.Literal['!no-unauthenticated'],
    t.Literal['dmca-violation'],
    t.Literal['doxxing'],
    t.Literal['porn'],
    t.Literal['sexual'],
    t.Literal['nudity'],
    t.Literal['nsfl'],
    t.Literal['gore'],
    str,
]  #: Label value
