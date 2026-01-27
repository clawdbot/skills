import typing as t

import typing_extensions as te
from pydantic import Field

if t.TYPE_CHECKING:
    from atproto_client import models
    from atproto_client.models import dot_dict

UnknownRecordType: te.TypeAlias = t.Union[
    'models.AppBskyActorProfile.Record',
    'models.AppBskyActorStatus.Record',
    'models.AppBskyFeedGenerator.Record',
    'models.AppBskyFeedLike.Record',
    'models.AppBskyFeedPost.Record',
    'models.AppBskyFeedPostgate.Record',
    'models.AppBskyFeedRepost.Record',
    'models.AppBskyFeedThreadgate.Record',
    'models.AppBskyGraphBlock.Record',
    'models.AppBskyGraphFollow.Record',
    'models.AppBskyGraphList.Record',
    'models.AppBskyGraphListblock.Record',
    'models.AppBskyGraphListitem.Record',
    'models.AppBskyGraphStarterpack.Record',
    'models.AppBskyGraphVerification.Record',
    'models.AppBskyLabelerService.Record',
    'models.AppBskyNotificationDeclaration.Record',
    'models.ChatBskyActorDeclaration.Record',
    'models.ComAtprotoLexiconSchema.Record',
]
UnknownRecordTypePydantic = te.Annotated[
    t.Union[
        'models.AppBskyActorProfile.Record',
        'models.AppBskyActorStatus.Record',
        'models.AppBskyFeedGenerator.Record',
        'models.AppBskyFeedLike.Record',
        'models.AppBskyFeedPost.Record',
        'models.AppBskyFeedPostgate.Record',
        'models.AppBskyFeedRepost.Record',
        'models.AppBskyFeedThreadgate.Record',
        'models.AppBskyGraphBlock.Record',
        'models.AppBskyGraphFollow.Record',
        'models.AppBskyGraphList.Record',
        'models.AppBskyGraphListblock.Record',
        'models.AppBskyGraphListitem.Record',
        'models.AppBskyGraphStarterpack.Record',
        'models.AppBskyGraphVerification.Record',
        'models.AppBskyLabelerService.Record',
        'models.AppBskyNotificationDeclaration.Record',
        'models.ChatBskyActorDeclaration.Record',
        'models.ComAtprotoLexiconSchema.Record',
    ],
    Field(discriminator='py_type'),
]
UnknownType: te.TypeAlias = t.Union[UnknownRecordTypePydantic, 'dot_dict.DotDictType']
UnknownInputType: te.TypeAlias = t.Union[UnknownType, t.Dict[str, t.Any]]
