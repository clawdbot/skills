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
    """Parameters model for :obj:`app.bsky.unspecced.searchPostsSkeleton`."""

    q: str  #: Search query string; syntax, phrase, boolean, and faceting is unspecified, but Lucene query syntax is recommended.
    author: t.Optional[string_formats.AtIdentifier] = (
        None  #: Filter to posts by the given account. Handles are resolved to DID before query-time.
    )
    cursor: t.Optional[str] = (
        None  #: Optional pagination mechanism; may not necessarily allow scrolling through entire result set.
    )
    domain: t.Optional[str] = (
        None  #: Filter to posts with URLs (facet links or embeds) linking to the given domain (hostname). Server may apply hostname normalization.
    )
    lang: t.Optional[string_formats.Language] = (
        None  #: Filter to posts in the given language. Expected to be based on post language field, though server may override language detection.
    )
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    mentions: t.Optional[string_formats.AtIdentifier] = (
        None  #: Filter to posts which mention the given account. Handles are resolved to DID before query-time. Only matches rich-text facet mentions.
    )
    since: t.Optional[str] = (
        None  #: Filter results for posts after the indicated datetime (inclusive). Expected to use 'sortAt' timestamp, which may not match 'createdAt'. Can be a datetime, or just an ISO date (YYYY-MM-DD).
    )
    sort: t.Optional[t.Union[t.Literal['top'], t.Literal['latest'], str]] = (
        'latest'  #: Specifies the ranking order of results.
    )
    tag: t.Optional[t.List[str]] = (
        None  #: Filter to posts with the given tag (hashtag), based on rich-text facet or tag field. Do not include the hash (#) prefix. Multiple tags can be specified, with 'AND' matching.
    )
    until: t.Optional[str] = (
        None  #: Filter results for posts before the indicated datetime (not inclusive). Expected to use 'sortAt' timestamp, which may not match 'createdAt'. Can be a datetime, or just an ISO date (YYY-MM-DD).
    )
    url: t.Optional[string_formats.Uri] = (
        None  #: Filter to posts with links (facet links or embeds) pointing to this URL. Server may apply URL normalization or fuzzy matching.
    )
    viewer: t.Optional[string_formats.Did] = (
        None  #: DID of the account making the request (not included for public/unauthenticated queries). Used for 'from:me' queries.
    )


class ParamsDict(t.TypedDict):
    q: str  #: Search query string; syntax, phrase, boolean, and faceting is unspecified, but Lucene query syntax is recommended.
    author: te.NotRequired[
        t.Optional[string_formats.AtIdentifier]
    ]  #: Filter to posts by the given account. Handles are resolved to DID before query-time.
    cursor: te.NotRequired[
        t.Optional[str]
    ]  #: Optional pagination mechanism; may not necessarily allow scrolling through entire result set.
    domain: te.NotRequired[
        t.Optional[str]
    ]  #: Filter to posts with URLs (facet links or embeds) linking to the given domain (hostname). Server may apply hostname normalization.
    lang: te.NotRequired[
        t.Optional[string_formats.Language]
    ]  #: Filter to posts in the given language. Expected to be based on post language field, though server may override language detection.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    mentions: te.NotRequired[
        t.Optional[string_formats.AtIdentifier]
    ]  #: Filter to posts which mention the given account. Handles are resolved to DID before query-time. Only matches rich-text facet mentions.
    since: te.NotRequired[
        t.Optional[str]
    ]  #: Filter results for posts after the indicated datetime (inclusive). Expected to use 'sortAt' timestamp, which may not match 'createdAt'. Can be a datetime, or just an ISO date (YYYY-MM-DD).
    sort: te.NotRequired[
        t.Optional[t.Union[t.Literal['top'], t.Literal['latest'], str]]
    ]  #: Specifies the ranking order of results.
    tag: te.NotRequired[
        t.Optional[t.List[str]]
    ]  #: Filter to posts with the given tag (hashtag), based on rich-text facet or tag field. Do not include the hash (#) prefix. Multiple tags can be specified, with 'AND' matching.
    until: te.NotRequired[
        t.Optional[str]
    ]  #: Filter results for posts before the indicated datetime (not inclusive). Expected to use 'sortAt' timestamp, which may not match 'createdAt'. Can be a datetime, or just an ISO date (YYY-MM-DD).
    url: te.NotRequired[
        t.Optional[string_formats.Uri]
    ]  #: Filter to posts with links (facet links or embeds) pointing to this URL. Server may apply URL normalization or fuzzy matching.
    viewer: te.NotRequired[
        t.Optional[string_formats.Did]
    ]  #: DID of the account making the request (not included for public/unauthenticated queries). Used for 'from:me' queries.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.unspecced.searchPostsSkeleton`."""

    posts: t.List['models.AppBskyUnspeccedDefs.SkeletonSearchPost']  #: Posts.
    cursor: t.Optional[str] = None  #: Cursor.
    hits_total: t.Optional[int] = (
        None  #: Count of search hits. Optional, may be rounded/truncated, and may not be possible to paginate through all hits.
    )
