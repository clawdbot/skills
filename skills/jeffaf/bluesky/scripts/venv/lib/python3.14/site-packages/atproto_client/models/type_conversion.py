from atproto_client import models

RECORD_TYPE_TO_MODEL_CLASS = {
    'app.bsky.actor.profile': models.AppBskyActorProfile.Record,
    'app.bsky.actor.status': models.AppBskyActorStatus.Record,
    'app.bsky.feed.generator': models.AppBskyFeedGenerator.Record,
    'app.bsky.feed.like': models.AppBskyFeedLike.Record,
    'app.bsky.feed.post': models.AppBskyFeedPost.Record,
    'app.bsky.feed.postgate': models.AppBskyFeedPostgate.Record,
    'app.bsky.feed.repost': models.AppBskyFeedRepost.Record,
    'app.bsky.feed.threadgate': models.AppBskyFeedThreadgate.Record,
    'app.bsky.graph.block': models.AppBskyGraphBlock.Record,
    'app.bsky.graph.follow': models.AppBskyGraphFollow.Record,
    'app.bsky.graph.list': models.AppBskyGraphList.Record,
    'app.bsky.graph.listblock': models.AppBskyGraphListblock.Record,
    'app.bsky.graph.listitem': models.AppBskyGraphListitem.Record,
    'app.bsky.graph.starterpack': models.AppBskyGraphStarterpack.Record,
    'app.bsky.graph.verification': models.AppBskyGraphVerification.Record,
    'app.bsky.labeler.service': models.AppBskyLabelerService.Record,
    'app.bsky.notification.declaration': models.AppBskyNotificationDeclaration.Record,
    'chat.bsky.actor.declaration': models.ChatBskyActorDeclaration.Record,
    'com.atproto.lexicon.schema': models.ComAtprotoLexiconSchema.Record,
}
