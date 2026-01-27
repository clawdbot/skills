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


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.admin.getSubjectStatus`."""

    blob: t.Optional[string_formats.Cid] = None  #: Blob.
    did: t.Optional[string_formats.Did] = None  #: Did.
    uri: t.Optional[string_formats.AtUri] = None  #: Uri.


class ParamsDict(t.TypedDict):
    blob: te.NotRequired[t.Optional[string_formats.Cid]]  #: Blob.
    did: te.NotRequired[t.Optional[string_formats.Did]]  #: Did.
    uri: te.NotRequired[t.Optional[string_formats.AtUri]]  #: Uri.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.admin.getSubjectStatus`."""

    subject: te.Annotated[
        t.Union[
            'models.ComAtprotoAdminDefs.RepoRef',
            'models.ComAtprotoRepoStrongRef.Main',
            'models.ComAtprotoAdminDefs.RepoBlobRef',
        ],
        Field(discriminator='py_type'),
    ]  #: Subject.
    deactivated: t.Optional['models.ComAtprotoAdminDefs.StatusAttr'] = None  #: Deactivated.
    takedown: t.Optional['models.ComAtprotoAdminDefs.StatusAttr'] = None  #: Takedown.
