##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base, string_formats


class Data(base.DataModelBase):
    """Input data model for :obj:`tools.ozone.communication.createTemplate`."""

    content_markdown: str  #: Content of the template, markdown supported, can contain variable placeholders.
    name: str  #: Name of the template.
    subject: str  #: Subject of the message, used in emails.
    created_by: t.Optional[string_formats.Did] = None  #: DID of the user who is creating the template.
    lang: t.Optional[string_formats.Language] = None  #: Message language.


class DataDict(t.TypedDict):
    content_markdown: str  #: Content of the template, markdown supported, can contain variable placeholders.
    name: str  #: Name of the template.
    subject: str  #: Subject of the message, used in emails.
    created_by: te.NotRequired[t.Optional[string_formats.Did]]  #: DID of the user who is creating the template.
    lang: te.NotRequired[t.Optional[string_formats.Language]]  #: Message language.
