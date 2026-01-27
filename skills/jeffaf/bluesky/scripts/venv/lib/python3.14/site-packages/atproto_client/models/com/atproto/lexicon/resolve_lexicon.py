##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.lexicon.resolveLexicon`."""

    nsid: string_formats.Nsid  #: The lexicon NSID to resolve.


class ParamsDict(t.TypedDict):
    nsid: string_formats.Nsid  #: The lexicon NSID to resolve.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.lexicon.resolveLexicon`."""

    cid: string_formats.Cid  #: The CID of the lexicon schema record.
    schema_: 'models.ComAtprotoLexiconSchema.Record'  #: The resolved lexicon schema record.
    uri: string_formats.AtUri  #: The AT-URI of the lexicon schema record.
