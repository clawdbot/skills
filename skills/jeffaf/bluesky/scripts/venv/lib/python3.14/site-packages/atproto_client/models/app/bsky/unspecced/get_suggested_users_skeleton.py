##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te
from pydantic import Field

from atproto_client.models import base, string_formats


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`app.bsky.unspecced.getSuggestedUsersSkeleton`."""

    category: t.Optional[str] = None  #: Category of users to get suggestions for.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=50)] = None  #: Limit.
    viewer: t.Optional[string_formats.Did] = (
        None  #: DID of the account making the request (not included for public/unauthenticated queries).
    )


class ParamsDict(t.TypedDict):
    category: te.NotRequired[t.Optional[str]]  #: Category of users to get suggestions for.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    viewer: te.NotRequired[
        t.Optional[string_formats.Did]
    ]  #: DID of the account making the request (not included for public/unauthenticated queries).


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.unspecced.getSuggestedUsersSkeleton`."""

    dids: t.List[string_formats.Did]  #: Dids.
