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


class Main(base.ModelBase):
    """Definition model for :obj:`app.bsky.richtext.facet`. Annotation of a sub-string within rich text."""

    features: t.List[
        te.Annotated[
            t.Union[
                'models.AppBskyRichtextFacet.Mention',
                'models.AppBskyRichtextFacet.Link',
                'models.AppBskyRichtextFacet.Tag',
            ],
            Field(discriminator='py_type'),
        ]
    ]  #: Features.
    index: 'models.AppBskyRichtextFacet.ByteSlice'  #: Index.

    py_type: t.Literal['app.bsky.richtext.facet'] = Field(default='app.bsky.richtext.facet', alias='$type', frozen=True)


class Mention(base.ModelBase):
    """Definition model for :obj:`app.bsky.richtext.facet`. Facet feature for mention of another account. The text is usually a handle, including a '@' prefix, but the facet reference is a DID."""

    did: string_formats.Did  #: Did.

    py_type: t.Literal['app.bsky.richtext.facet#mention'] = Field(
        default='app.bsky.richtext.facet#mention', alias='$type', frozen=True
    )


class Link(base.ModelBase):
    """Definition model for :obj:`app.bsky.richtext.facet`. Facet feature for a URL. The text URL may have been simplified or truncated, but the facet reference should be a complete URL."""

    uri: string_formats.Uri  #: Uri.

    py_type: t.Literal['app.bsky.richtext.facet#link'] = Field(
        default='app.bsky.richtext.facet#link', alias='$type', frozen=True
    )


class Tag(base.ModelBase):
    """Definition model for :obj:`app.bsky.richtext.facet`. Facet feature for a hashtag. The text usually includes a '#' prefix, but the facet reference should not (except in the case of 'double hash tags')."""

    tag: str = Field(max_length=640)  #: Tag.

    py_type: t.Literal['app.bsky.richtext.facet#tag'] = Field(
        default='app.bsky.richtext.facet#tag', alias='$type', frozen=True
    )


class ByteSlice(base.ModelBase):
    """Definition model for :obj:`app.bsky.richtext.facet`. Specifies the sub-string range a facet feature applies to. Start index is inclusive, end index is exclusive. Indices are zero-indexed, counting bytes of the UTF-8 encoded text. NOTE: some languages, like Javascript, use UTF-16 or Unicode codepoints for string slice indexing; in these languages, convert to byte arrays before working with facets."""

    byte_end: int = Field(ge=0)  #: Byte end.
    byte_start: int = Field(ge=0)  #: Byte start.

    py_type: t.Literal['app.bsky.richtext.facet#byteSlice'] = Field(
        default='app.bsky.richtext.facet#byteSlice', alias='$type', frozen=True
    )
