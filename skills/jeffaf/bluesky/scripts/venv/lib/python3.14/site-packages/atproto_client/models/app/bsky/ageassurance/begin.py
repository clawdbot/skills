##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`app.bsky.ageassurance.begin`."""

    country_code: str  #: An ISO 3166-1 alpha-2 code of the user's location.
    email: str  #: The user's email address to receive Age Assurance instructions.
    language: str  #: The user's preferred language for communication during the Age Assurance process.
    region_code: t.Optional[str] = (
        None  #: An optional ISO 3166-2 code of the user's region or state within the country.
    )


class DataDict(t.TypedDict):
    country_code: str  #: An ISO 3166-1 alpha-2 code of the user's location.
    email: str  #: The user's email address to receive Age Assurance instructions.
    language: str  #: The user's preferred language for communication during the Age Assurance process.
    region_code: te.NotRequired[
        t.Optional[str]
    ]  #: An optional ISO 3166-2 code of the user's region or state within the country.
