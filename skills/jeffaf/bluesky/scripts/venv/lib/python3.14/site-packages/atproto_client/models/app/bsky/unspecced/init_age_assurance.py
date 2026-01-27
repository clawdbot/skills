##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`app.bsky.unspecced.initAgeAssurance`."""

    country_code: str  #: An ISO 3166-1 alpha-2 code of the user's location.
    email: str  #: The user's email address to receive assurance instructions.
    language: str  #: The user's preferred language for communication during the assurance process.


class DataDict(t.TypedDict):
    country_code: str  #: An ISO 3166-1 alpha-2 code of the user's location.
    email: str  #: The user's email address to receive assurance instructions.
    language: str  #: The user's preferred language for communication during the assurance process.
