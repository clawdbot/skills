from atproto_client.models.app.bsky.actor import defs as AppBskyActorDefs
from atproto_client.models.app.bsky.actor import get_preferences as AppBskyActorGetPreferences
from atproto_client.models.app.bsky.actor import get_profile as AppBskyActorGetProfile
from atproto_client.models.app.bsky.actor import get_profiles as AppBskyActorGetProfiles
from atproto_client.models.app.bsky.actor import get_suggestions as AppBskyActorGetSuggestions
from atproto_client.models.app.bsky.actor import profile as AppBskyActorProfile
from atproto_client.models.app.bsky.actor import put_preferences as AppBskyActorPutPreferences
from atproto_client.models.app.bsky.actor import search_actors as AppBskyActorSearchActors
from atproto_client.models.app.bsky.actor import search_actors_typeahead as AppBskyActorSearchActorsTypeahead
from atproto_client.models.app.bsky.actor import status as AppBskyActorStatus
from atproto_client.models.app.bsky.ageassurance import begin as AppBskyAgeassuranceBegin
from atproto_client.models.app.bsky.ageassurance import defs as AppBskyAgeassuranceDefs
from atproto_client.models.app.bsky.ageassurance import get_config as AppBskyAgeassuranceGetConfig
from atproto_client.models.app.bsky.ageassurance import get_state as AppBskyAgeassuranceGetState
from atproto_client.models.app.bsky.bookmark import create_bookmark as AppBskyBookmarkCreateBookmark
from atproto_client.models.app.bsky.bookmark import defs as AppBskyBookmarkDefs
from atproto_client.models.app.bsky.bookmark import delete_bookmark as AppBskyBookmarkDeleteBookmark
from atproto_client.models.app.bsky.bookmark import get_bookmarks as AppBskyBookmarkGetBookmarks
from atproto_client.models.app.bsky.contact import defs as AppBskyContactDefs
from atproto_client.models.app.bsky.contact import dismiss_match as AppBskyContactDismissMatch
from atproto_client.models.app.bsky.contact import get_matches as AppBskyContactGetMatches
from atproto_client.models.app.bsky.contact import get_sync_status as AppBskyContactGetSyncStatus
from atproto_client.models.app.bsky.contact import import_contacts as AppBskyContactImportContacts
from atproto_client.models.app.bsky.contact import remove_data as AppBskyContactRemoveData
from atproto_client.models.app.bsky.contact import start_phone_verification as AppBskyContactStartPhoneVerification
from atproto_client.models.app.bsky.contact import verify_phone as AppBskyContactVerifyPhone
from atproto_client.models.app.bsky.embed import defs as AppBskyEmbedDefs
from atproto_client.models.app.bsky.embed import external as AppBskyEmbedExternal
from atproto_client.models.app.bsky.embed import images as AppBskyEmbedImages
from atproto_client.models.app.bsky.embed import record as AppBskyEmbedRecord
from atproto_client.models.app.bsky.embed import record_with_media as AppBskyEmbedRecordWithMedia
from atproto_client.models.app.bsky.embed import video as AppBskyEmbedVideo
from atproto_client.models.app.bsky.feed import defs as AppBskyFeedDefs
from atproto_client.models.app.bsky.feed import describe_feed_generator as AppBskyFeedDescribeFeedGenerator
from atproto_client.models.app.bsky.feed import generator as AppBskyFeedGenerator
from atproto_client.models.app.bsky.feed import get_actor_feeds as AppBskyFeedGetActorFeeds
from atproto_client.models.app.bsky.feed import get_actor_likes as AppBskyFeedGetActorLikes
from atproto_client.models.app.bsky.feed import get_author_feed as AppBskyFeedGetAuthorFeed
from atproto_client.models.app.bsky.feed import get_feed as AppBskyFeedGetFeed
from atproto_client.models.app.bsky.feed import get_feed_generator as AppBskyFeedGetFeedGenerator
from atproto_client.models.app.bsky.feed import get_feed_generators as AppBskyFeedGetFeedGenerators
from atproto_client.models.app.bsky.feed import get_feed_skeleton as AppBskyFeedGetFeedSkeleton
from atproto_client.models.app.bsky.feed import get_likes as AppBskyFeedGetLikes
from atproto_client.models.app.bsky.feed import get_list_feed as AppBskyFeedGetListFeed
from atproto_client.models.app.bsky.feed import get_post_thread as AppBskyFeedGetPostThread
from atproto_client.models.app.bsky.feed import get_posts as AppBskyFeedGetPosts
from atproto_client.models.app.bsky.feed import get_quotes as AppBskyFeedGetQuotes
from atproto_client.models.app.bsky.feed import get_reposted_by as AppBskyFeedGetRepostedBy
from atproto_client.models.app.bsky.feed import get_suggested_feeds as AppBskyFeedGetSuggestedFeeds
from atproto_client.models.app.bsky.feed import get_timeline as AppBskyFeedGetTimeline
from atproto_client.models.app.bsky.feed import like as AppBskyFeedLike
from atproto_client.models.app.bsky.feed import post as AppBskyFeedPost
from atproto_client.models.app.bsky.feed import postgate as AppBskyFeedPostgate
from atproto_client.models.app.bsky.feed import repost as AppBskyFeedRepost
from atproto_client.models.app.bsky.feed import search_posts as AppBskyFeedSearchPosts
from atproto_client.models.app.bsky.feed import send_interactions as AppBskyFeedSendInteractions
from atproto_client.models.app.bsky.feed import threadgate as AppBskyFeedThreadgate
from atproto_client.models.app.bsky.graph import block as AppBskyGraphBlock
from atproto_client.models.app.bsky.graph import defs as AppBskyGraphDefs
from atproto_client.models.app.bsky.graph import follow as AppBskyGraphFollow
from atproto_client.models.app.bsky.graph import get_actor_starter_packs as AppBskyGraphGetActorStarterPacks
from atproto_client.models.app.bsky.graph import get_blocks as AppBskyGraphGetBlocks
from atproto_client.models.app.bsky.graph import get_followers as AppBskyGraphGetFollowers
from atproto_client.models.app.bsky.graph import get_follows as AppBskyGraphGetFollows
from atproto_client.models.app.bsky.graph import get_known_followers as AppBskyGraphGetKnownFollowers
from atproto_client.models.app.bsky.graph import get_list as AppBskyGraphGetList
from atproto_client.models.app.bsky.graph import get_list_blocks as AppBskyGraphGetListBlocks
from atproto_client.models.app.bsky.graph import get_list_mutes as AppBskyGraphGetListMutes
from atproto_client.models.app.bsky.graph import get_lists as AppBskyGraphGetLists
from atproto_client.models.app.bsky.graph import get_lists_with_membership as AppBskyGraphGetListsWithMembership
from atproto_client.models.app.bsky.graph import get_mutes as AppBskyGraphGetMutes
from atproto_client.models.app.bsky.graph import get_relationships as AppBskyGraphGetRelationships
from atproto_client.models.app.bsky.graph import get_starter_pack as AppBskyGraphGetStarterPack
from atproto_client.models.app.bsky.graph import get_starter_packs as AppBskyGraphGetStarterPacks
from atproto_client.models.app.bsky.graph import (
    get_starter_packs_with_membership as AppBskyGraphGetStarterPacksWithMembership,
)
from atproto_client.models.app.bsky.graph import (
    get_suggested_follows_by_actor as AppBskyGraphGetSuggestedFollowsByActor,
)
from atproto_client.models.app.bsky.graph import list as AppBskyGraphList
from atproto_client.models.app.bsky.graph import listblock as AppBskyGraphListblock
from atproto_client.models.app.bsky.graph import listitem as AppBskyGraphListitem
from atproto_client.models.app.bsky.graph import mute_actor as AppBskyGraphMuteActor
from atproto_client.models.app.bsky.graph import mute_actor_list as AppBskyGraphMuteActorList
from atproto_client.models.app.bsky.graph import mute_thread as AppBskyGraphMuteThread
from atproto_client.models.app.bsky.graph import search_starter_packs as AppBskyGraphSearchStarterPacks
from atproto_client.models.app.bsky.graph import starterpack as AppBskyGraphStarterpack
from atproto_client.models.app.bsky.graph import unmute_actor as AppBskyGraphUnmuteActor
from atproto_client.models.app.bsky.graph import unmute_actor_list as AppBskyGraphUnmuteActorList
from atproto_client.models.app.bsky.graph import unmute_thread as AppBskyGraphUnmuteThread
from atproto_client.models.app.bsky.graph import verification as AppBskyGraphVerification
from atproto_client.models.app.bsky.labeler import defs as AppBskyLabelerDefs
from atproto_client.models.app.bsky.labeler import get_services as AppBskyLabelerGetServices
from atproto_client.models.app.bsky.labeler import service as AppBskyLabelerService
from atproto_client.models.app.bsky.notification import declaration as AppBskyNotificationDeclaration
from atproto_client.models.app.bsky.notification import defs as AppBskyNotificationDefs
from atproto_client.models.app.bsky.notification import get_preferences as AppBskyNotificationGetPreferences
from atproto_client.models.app.bsky.notification import get_unread_count as AppBskyNotificationGetUnreadCount
from atproto_client.models.app.bsky.notification import (
    list_activity_subscriptions as AppBskyNotificationListActivitySubscriptions,
)
from atproto_client.models.app.bsky.notification import list_notifications as AppBskyNotificationListNotifications
from atproto_client.models.app.bsky.notification import (
    put_activity_subscription as AppBskyNotificationPutActivitySubscription,
)
from atproto_client.models.app.bsky.notification import put_preferences as AppBskyNotificationPutPreferences
from atproto_client.models.app.bsky.notification import put_preferences_v2 as AppBskyNotificationPutPreferencesV2
from atproto_client.models.app.bsky.notification import register_push as AppBskyNotificationRegisterPush
from atproto_client.models.app.bsky.notification import unregister_push as AppBskyNotificationUnregisterPush
from atproto_client.models.app.bsky.notification import update_seen as AppBskyNotificationUpdateSeen
from atproto_client.models.app.bsky.richtext import facet as AppBskyRichtextFacet
from atproto_client.models.app.bsky.unspecced import defs as AppBskyUnspeccedDefs
from atproto_client.models.app.bsky.unspecced import get_age_assurance_state as AppBskyUnspeccedGetAgeAssuranceState
from atproto_client.models.app.bsky.unspecced import get_config as AppBskyUnspeccedGetConfig
from atproto_client.models.app.bsky.unspecced import (
    get_onboarding_suggested_starter_packs as AppBskyUnspeccedGetOnboardingSuggestedStarterPacks,
)
from atproto_client.models.app.bsky.unspecced import (
    get_onboarding_suggested_starter_packs_skeleton as AppBskyUnspeccedGetOnboardingSuggestedStarterPacksSkeleton,
)
from atproto_client.models.app.bsky.unspecced import (
    get_popular_feed_generators as AppBskyUnspeccedGetPopularFeedGenerators,
)
from atproto_client.models.app.bsky.unspecced import get_post_thread_other_v2 as AppBskyUnspeccedGetPostThreadOtherV2
from atproto_client.models.app.bsky.unspecced import get_post_thread_v2 as AppBskyUnspeccedGetPostThreadV2
from atproto_client.models.app.bsky.unspecced import get_suggested_feeds as AppBskyUnspeccedGetSuggestedFeeds
from atproto_client.models.app.bsky.unspecced import (
    get_suggested_feeds_skeleton as AppBskyUnspeccedGetSuggestedFeedsSkeleton,
)
from atproto_client.models.app.bsky.unspecced import (
    get_suggested_starter_packs as AppBskyUnspeccedGetSuggestedStarterPacks,
)
from atproto_client.models.app.bsky.unspecced import (
    get_suggested_starter_packs_skeleton as AppBskyUnspeccedGetSuggestedStarterPacksSkeleton,
)
from atproto_client.models.app.bsky.unspecced import get_suggested_users as AppBskyUnspeccedGetSuggestedUsers
from atproto_client.models.app.bsky.unspecced import (
    get_suggested_users_skeleton as AppBskyUnspeccedGetSuggestedUsersSkeleton,
)
from atproto_client.models.app.bsky.unspecced import get_suggestions_skeleton as AppBskyUnspeccedGetSuggestionsSkeleton
from atproto_client.models.app.bsky.unspecced import get_tagged_suggestions as AppBskyUnspeccedGetTaggedSuggestions
from atproto_client.models.app.bsky.unspecced import get_trending_topics as AppBskyUnspeccedGetTrendingTopics
from atproto_client.models.app.bsky.unspecced import get_trends as AppBskyUnspeccedGetTrends
from atproto_client.models.app.bsky.unspecced import get_trends_skeleton as AppBskyUnspeccedGetTrendsSkeleton
from atproto_client.models.app.bsky.unspecced import init_age_assurance as AppBskyUnspeccedInitAgeAssurance
from atproto_client.models.app.bsky.unspecced import search_actors_skeleton as AppBskyUnspeccedSearchActorsSkeleton
from atproto_client.models.app.bsky.unspecced import search_posts_skeleton as AppBskyUnspeccedSearchPostsSkeleton
from atproto_client.models.app.bsky.unspecced import (
    search_starter_packs_skeleton as AppBskyUnspeccedSearchStarterPacksSkeleton,
)
from atproto_client.models.app.bsky.video import defs as AppBskyVideoDefs
from atproto_client.models.app.bsky.video import get_job_status as AppBskyVideoGetJobStatus
from atproto_client.models.app.bsky.video import get_upload_limits as AppBskyVideoGetUploadLimits
from atproto_client.models.app.bsky.video import upload_video as AppBskyVideoUploadVideo
from atproto_client.models.chat.bsky.actor import declaration as ChatBskyActorDeclaration
from atproto_client.models.chat.bsky.actor import defs as ChatBskyActorDefs
from atproto_client.models.chat.bsky.actor import delete_account as ChatBskyActorDeleteAccount
from atproto_client.models.chat.bsky.actor import export_account_data as ChatBskyActorExportAccountData
from atproto_client.models.chat.bsky.convo import accept_convo as ChatBskyConvoAcceptConvo
from atproto_client.models.chat.bsky.convo import add_reaction as ChatBskyConvoAddReaction
from atproto_client.models.chat.bsky.convo import defs as ChatBskyConvoDefs
from atproto_client.models.chat.bsky.convo import delete_message_for_self as ChatBskyConvoDeleteMessageForSelf
from atproto_client.models.chat.bsky.convo import get_convo as ChatBskyConvoGetConvo
from atproto_client.models.chat.bsky.convo import get_convo_availability as ChatBskyConvoGetConvoAvailability
from atproto_client.models.chat.bsky.convo import get_convo_for_members as ChatBskyConvoGetConvoForMembers
from atproto_client.models.chat.bsky.convo import get_log as ChatBskyConvoGetLog
from atproto_client.models.chat.bsky.convo import get_messages as ChatBskyConvoGetMessages
from atproto_client.models.chat.bsky.convo import leave_convo as ChatBskyConvoLeaveConvo
from atproto_client.models.chat.bsky.convo import list_convos as ChatBskyConvoListConvos
from atproto_client.models.chat.bsky.convo import mute_convo as ChatBskyConvoMuteConvo
from atproto_client.models.chat.bsky.convo import remove_reaction as ChatBskyConvoRemoveReaction
from atproto_client.models.chat.bsky.convo import send_message as ChatBskyConvoSendMessage
from atproto_client.models.chat.bsky.convo import send_message_batch as ChatBskyConvoSendMessageBatch
from atproto_client.models.chat.bsky.convo import unmute_convo as ChatBskyConvoUnmuteConvo
from atproto_client.models.chat.bsky.convo import update_all_read as ChatBskyConvoUpdateAllRead
from atproto_client.models.chat.bsky.convo import update_read as ChatBskyConvoUpdateRead
from atproto_client.models.chat.bsky.moderation import get_actor_metadata as ChatBskyModerationGetActorMetadata
from atproto_client.models.chat.bsky.moderation import get_message_context as ChatBskyModerationGetMessageContext
from atproto_client.models.chat.bsky.moderation import update_actor_access as ChatBskyModerationUpdateActorAccess
from atproto_client.models.com.atproto.admin import defs as ComAtprotoAdminDefs
from atproto_client.models.com.atproto.admin import delete_account as ComAtprotoAdminDeleteAccount
from atproto_client.models.com.atproto.admin import disable_account_invites as ComAtprotoAdminDisableAccountInvites
from atproto_client.models.com.atproto.admin import disable_invite_codes as ComAtprotoAdminDisableInviteCodes
from atproto_client.models.com.atproto.admin import enable_account_invites as ComAtprotoAdminEnableAccountInvites
from atproto_client.models.com.atproto.admin import get_account_info as ComAtprotoAdminGetAccountInfo
from atproto_client.models.com.atproto.admin import get_account_infos as ComAtprotoAdminGetAccountInfos
from atproto_client.models.com.atproto.admin import get_invite_codes as ComAtprotoAdminGetInviteCodes
from atproto_client.models.com.atproto.admin import get_subject_status as ComAtprotoAdminGetSubjectStatus
from atproto_client.models.com.atproto.admin import search_accounts as ComAtprotoAdminSearchAccounts
from atproto_client.models.com.atproto.admin import send_email as ComAtprotoAdminSendEmail
from atproto_client.models.com.atproto.admin import update_account_email as ComAtprotoAdminUpdateAccountEmail
from atproto_client.models.com.atproto.admin import update_account_handle as ComAtprotoAdminUpdateAccountHandle
from atproto_client.models.com.atproto.admin import update_account_password as ComAtprotoAdminUpdateAccountPassword
from atproto_client.models.com.atproto.admin import update_account_signing_key as ComAtprotoAdminUpdateAccountSigningKey
from atproto_client.models.com.atproto.admin import update_subject_status as ComAtprotoAdminUpdateSubjectStatus
from atproto_client.models.com.atproto.identity import defs as ComAtprotoIdentityDefs
from atproto_client.models.com.atproto.identity import (
    get_recommended_did_credentials as ComAtprotoIdentityGetRecommendedDidCredentials,
)
from atproto_client.models.com.atproto.identity import refresh_identity as ComAtprotoIdentityRefreshIdentity
from atproto_client.models.com.atproto.identity import (
    request_plc_operation_signature as ComAtprotoIdentityRequestPlcOperationSignature,
)
from atproto_client.models.com.atproto.identity import resolve_did as ComAtprotoIdentityResolveDid
from atproto_client.models.com.atproto.identity import resolve_handle as ComAtprotoIdentityResolveHandle
from atproto_client.models.com.atproto.identity import resolve_identity as ComAtprotoIdentityResolveIdentity
from atproto_client.models.com.atproto.identity import sign_plc_operation as ComAtprotoIdentitySignPlcOperation
from atproto_client.models.com.atproto.identity import submit_plc_operation as ComAtprotoIdentitySubmitPlcOperation
from atproto_client.models.com.atproto.identity import update_handle as ComAtprotoIdentityUpdateHandle
from atproto_client.models.com.atproto.label import defs as ComAtprotoLabelDefs
from atproto_client.models.com.atproto.label import query_labels as ComAtprotoLabelQueryLabels
from atproto_client.models.com.atproto.label import subscribe_labels as ComAtprotoLabelSubscribeLabels
from atproto_client.models.com.atproto.lexicon import resolve_lexicon as ComAtprotoLexiconResolveLexicon
from atproto_client.models.com.atproto.lexicon import schema as ComAtprotoLexiconSchema
from atproto_client.models.com.atproto.moderation import create_report as ComAtprotoModerationCreateReport
from atproto_client.models.com.atproto.moderation import defs as ComAtprotoModerationDefs
from atproto_client.models.com.atproto.repo import apply_writes as ComAtprotoRepoApplyWrites
from atproto_client.models.com.atproto.repo import create_record as ComAtprotoRepoCreateRecord
from atproto_client.models.com.atproto.repo import defs as ComAtprotoRepoDefs
from atproto_client.models.com.atproto.repo import delete_record as ComAtprotoRepoDeleteRecord
from atproto_client.models.com.atproto.repo import describe_repo as ComAtprotoRepoDescribeRepo
from atproto_client.models.com.atproto.repo import get_record as ComAtprotoRepoGetRecord
from atproto_client.models.com.atproto.repo import import_repo as ComAtprotoRepoImportRepo
from atproto_client.models.com.atproto.repo import list_missing_blobs as ComAtprotoRepoListMissingBlobs
from atproto_client.models.com.atproto.repo import list_records as ComAtprotoRepoListRecords
from atproto_client.models.com.atproto.repo import put_record as ComAtprotoRepoPutRecord
from atproto_client.models.com.atproto.repo import strong_ref as ComAtprotoRepoStrongRef
from atproto_client.models.com.atproto.repo import upload_blob as ComAtprotoRepoUploadBlob
from atproto_client.models.com.atproto.server import activate_account as ComAtprotoServerActivateAccount
from atproto_client.models.com.atproto.server import check_account_status as ComAtprotoServerCheckAccountStatus
from atproto_client.models.com.atproto.server import confirm_email as ComAtprotoServerConfirmEmail
from atproto_client.models.com.atproto.server import create_account as ComAtprotoServerCreateAccount
from atproto_client.models.com.atproto.server import create_app_password as ComAtprotoServerCreateAppPassword
from atproto_client.models.com.atproto.server import create_invite_code as ComAtprotoServerCreateInviteCode
from atproto_client.models.com.atproto.server import create_invite_codes as ComAtprotoServerCreateInviteCodes
from atproto_client.models.com.atproto.server import create_session as ComAtprotoServerCreateSession
from atproto_client.models.com.atproto.server import deactivate_account as ComAtprotoServerDeactivateAccount
from atproto_client.models.com.atproto.server import defs as ComAtprotoServerDefs
from atproto_client.models.com.atproto.server import delete_account as ComAtprotoServerDeleteAccount
from atproto_client.models.com.atproto.server import delete_session as ComAtprotoServerDeleteSession
from atproto_client.models.com.atproto.server import describe_server as ComAtprotoServerDescribeServer
from atproto_client.models.com.atproto.server import get_account_invite_codes as ComAtprotoServerGetAccountInviteCodes
from atproto_client.models.com.atproto.server import get_service_auth as ComAtprotoServerGetServiceAuth
from atproto_client.models.com.atproto.server import get_session as ComAtprotoServerGetSession
from atproto_client.models.com.atproto.server import list_app_passwords as ComAtprotoServerListAppPasswords
from atproto_client.models.com.atproto.server import refresh_session as ComAtprotoServerRefreshSession
from atproto_client.models.com.atproto.server import request_account_delete as ComAtprotoServerRequestAccountDelete
from atproto_client.models.com.atproto.server import (
    request_email_confirmation as ComAtprotoServerRequestEmailConfirmation,
)
from atproto_client.models.com.atproto.server import request_email_update as ComAtprotoServerRequestEmailUpdate
from atproto_client.models.com.atproto.server import request_password_reset as ComAtprotoServerRequestPasswordReset
from atproto_client.models.com.atproto.server import reserve_signing_key as ComAtprotoServerReserveSigningKey
from atproto_client.models.com.atproto.server import reset_password as ComAtprotoServerResetPassword
from atproto_client.models.com.atproto.server import revoke_app_password as ComAtprotoServerRevokeAppPassword
from atproto_client.models.com.atproto.server import update_email as ComAtprotoServerUpdateEmail
from atproto_client.models.com.atproto.sync import defs as ComAtprotoSyncDefs
from atproto_client.models.com.atproto.sync import get_blob as ComAtprotoSyncGetBlob
from atproto_client.models.com.atproto.sync import get_blocks as ComAtprotoSyncGetBlocks
from atproto_client.models.com.atproto.sync import get_checkout as ComAtprotoSyncGetCheckout
from atproto_client.models.com.atproto.sync import get_head as ComAtprotoSyncGetHead
from atproto_client.models.com.atproto.sync import get_host_status as ComAtprotoSyncGetHostStatus
from atproto_client.models.com.atproto.sync import get_latest_commit as ComAtprotoSyncGetLatestCommit
from atproto_client.models.com.atproto.sync import get_record as ComAtprotoSyncGetRecord
from atproto_client.models.com.atproto.sync import get_repo as ComAtprotoSyncGetRepo
from atproto_client.models.com.atproto.sync import get_repo_status as ComAtprotoSyncGetRepoStatus
from atproto_client.models.com.atproto.sync import list_blobs as ComAtprotoSyncListBlobs
from atproto_client.models.com.atproto.sync import list_hosts as ComAtprotoSyncListHosts
from atproto_client.models.com.atproto.sync import list_repos as ComAtprotoSyncListRepos
from atproto_client.models.com.atproto.sync import list_repos_by_collection as ComAtprotoSyncListReposByCollection
from atproto_client.models.com.atproto.sync import notify_of_update as ComAtprotoSyncNotifyOfUpdate
from atproto_client.models.com.atproto.sync import request_crawl as ComAtprotoSyncRequestCrawl
from atproto_client.models.com.atproto.sync import subscribe_repos as ComAtprotoSyncSubscribeRepos
from atproto_client.models.com.atproto.temp import add_reserved_handle as ComAtprotoTempAddReservedHandle
from atproto_client.models.com.atproto.temp import check_handle_availability as ComAtprotoTempCheckHandleAvailability
from atproto_client.models.com.atproto.temp import check_signup_queue as ComAtprotoTempCheckSignupQueue
from atproto_client.models.com.atproto.temp import dereference_scope as ComAtprotoTempDereferenceScope
from atproto_client.models.com.atproto.temp import fetch_labels as ComAtprotoTempFetchLabels
from atproto_client.models.com.atproto.temp import request_phone_verification as ComAtprotoTempRequestPhoneVerification
from atproto_client.models.com.atproto.temp import revoke_account_credentials as ComAtprotoTempRevokeAccountCredentials
from atproto_client.models.models_loader import load_models
from atproto_client.models.tools.ozone.communication import create_template as ToolsOzoneCommunicationCreateTemplate
from atproto_client.models.tools.ozone.communication import defs as ToolsOzoneCommunicationDefs
from atproto_client.models.tools.ozone.communication import delete_template as ToolsOzoneCommunicationDeleteTemplate
from atproto_client.models.tools.ozone.communication import list_templates as ToolsOzoneCommunicationListTemplates
from atproto_client.models.tools.ozone.communication import update_template as ToolsOzoneCommunicationUpdateTemplate
from atproto_client.models.tools.ozone.hosting import get_account_history as ToolsOzoneHostingGetAccountHistory
from atproto_client.models.tools.ozone.moderation import (
    cancel_scheduled_actions as ToolsOzoneModerationCancelScheduledActions,
)
from atproto_client.models.tools.ozone.moderation import defs as ToolsOzoneModerationDefs
from atproto_client.models.tools.ozone.moderation import emit_event as ToolsOzoneModerationEmitEvent
from atproto_client.models.tools.ozone.moderation import get_account_timeline as ToolsOzoneModerationGetAccountTimeline
from atproto_client.models.tools.ozone.moderation import get_event as ToolsOzoneModerationGetEvent
from atproto_client.models.tools.ozone.moderation import get_record as ToolsOzoneModerationGetRecord
from atproto_client.models.tools.ozone.moderation import get_records as ToolsOzoneModerationGetRecords
from atproto_client.models.tools.ozone.moderation import get_repo as ToolsOzoneModerationGetRepo
from atproto_client.models.tools.ozone.moderation import get_reporter_stats as ToolsOzoneModerationGetReporterStats
from atproto_client.models.tools.ozone.moderation import get_repos as ToolsOzoneModerationGetRepos
from atproto_client.models.tools.ozone.moderation import get_subjects as ToolsOzoneModerationGetSubjects
from atproto_client.models.tools.ozone.moderation import (
    list_scheduled_actions as ToolsOzoneModerationListScheduledActions,
)
from atproto_client.models.tools.ozone.moderation import query_events as ToolsOzoneModerationQueryEvents
from atproto_client.models.tools.ozone.moderation import query_statuses as ToolsOzoneModerationQueryStatuses
from atproto_client.models.tools.ozone.moderation import schedule_action as ToolsOzoneModerationScheduleAction
from atproto_client.models.tools.ozone.moderation import search_repos as ToolsOzoneModerationSearchRepos
from atproto_client.models.tools.ozone.report import defs as ToolsOzoneReportDefs
from atproto_client.models.tools.ozone.safelink import add_rule as ToolsOzoneSafelinkAddRule
from atproto_client.models.tools.ozone.safelink import defs as ToolsOzoneSafelinkDefs
from atproto_client.models.tools.ozone.safelink import query_events as ToolsOzoneSafelinkQueryEvents
from atproto_client.models.tools.ozone.safelink import query_rules as ToolsOzoneSafelinkQueryRules
from atproto_client.models.tools.ozone.safelink import remove_rule as ToolsOzoneSafelinkRemoveRule
from atproto_client.models.tools.ozone.safelink import update_rule as ToolsOzoneSafelinkUpdateRule
from atproto_client.models.tools.ozone.server import get_config as ToolsOzoneServerGetConfig
from atproto_client.models.tools.ozone.set import add_values as ToolsOzoneSetAddValues
from atproto_client.models.tools.ozone.set import defs as ToolsOzoneSetDefs
from atproto_client.models.tools.ozone.set import delete_set as ToolsOzoneSetDeleteSet
from atproto_client.models.tools.ozone.set import delete_values as ToolsOzoneSetDeleteValues
from atproto_client.models.tools.ozone.set import get_values as ToolsOzoneSetGetValues
from atproto_client.models.tools.ozone.set import query_sets as ToolsOzoneSetQuerySets
from atproto_client.models.tools.ozone.set import upsert_set as ToolsOzoneSetUpsertSet
from atproto_client.models.tools.ozone.setting import defs as ToolsOzoneSettingDefs
from atproto_client.models.tools.ozone.setting import list_options as ToolsOzoneSettingListOptions
from atproto_client.models.tools.ozone.setting import remove_options as ToolsOzoneSettingRemoveOptions
from atproto_client.models.tools.ozone.setting import upsert_option as ToolsOzoneSettingUpsertOption
from atproto_client.models.tools.ozone.signature import defs as ToolsOzoneSignatureDefs
from atproto_client.models.tools.ozone.signature import find_correlation as ToolsOzoneSignatureFindCorrelation
from atproto_client.models.tools.ozone.signature import find_related_accounts as ToolsOzoneSignatureFindRelatedAccounts
from atproto_client.models.tools.ozone.signature import search_accounts as ToolsOzoneSignatureSearchAccounts
from atproto_client.models.tools.ozone.team import add_member as ToolsOzoneTeamAddMember
from atproto_client.models.tools.ozone.team import defs as ToolsOzoneTeamDefs
from atproto_client.models.tools.ozone.team import delete_member as ToolsOzoneTeamDeleteMember
from atproto_client.models.tools.ozone.team import list_members as ToolsOzoneTeamListMembers
from atproto_client.models.tools.ozone.team import update_member as ToolsOzoneTeamUpdateMember
from atproto_client.models.tools.ozone.verification import defs as ToolsOzoneVerificationDefs
from atproto_client.models.tools.ozone.verification import (
    grant_verifications as ToolsOzoneVerificationGrantVerifications,
)
from atproto_client.models.tools.ozone.verification import list_verifications as ToolsOzoneVerificationListVerifications
from atproto_client.models.tools.ozone.verification import (
    revoke_verifications as ToolsOzoneVerificationRevokeVerifications,
)
from atproto_client.models.utils import (
    create_strong_ref,
    get_model_as_dict,
    get_model_as_json,
    get_or_create,
    is_record_type,
)


class _Ids:
    AppBskyActorDefs: str = 'app.bsky.actor.defs'
    AppBskyActorGetPreferences: str = 'app.bsky.actor.getPreferences'
    AppBskyActorGetProfile: str = 'app.bsky.actor.getProfile'
    AppBskyActorGetProfiles: str = 'app.bsky.actor.getProfiles'
    AppBskyActorGetSuggestions: str = 'app.bsky.actor.getSuggestions'
    AppBskyActorProfile: str = 'app.bsky.actor.profile'
    AppBskyActorPutPreferences: str = 'app.bsky.actor.putPreferences'
    AppBskyActorSearchActors: str = 'app.bsky.actor.searchActors'
    AppBskyActorSearchActorsTypeahead: str = 'app.bsky.actor.searchActorsTypeahead'
    AppBskyActorStatus: str = 'app.bsky.actor.status'
    AppBskyAgeassuranceBegin: str = 'app.bsky.ageassurance.begin'
    AppBskyAgeassuranceDefs: str = 'app.bsky.ageassurance.defs'
    AppBskyAgeassuranceGetConfig: str = 'app.bsky.ageassurance.getConfig'
    AppBskyAgeassuranceGetState: str = 'app.bsky.ageassurance.getState'
    AppBskyBookmarkCreateBookmark: str = 'app.bsky.bookmark.createBookmark'
    AppBskyBookmarkDefs: str = 'app.bsky.bookmark.defs'
    AppBskyBookmarkDeleteBookmark: str = 'app.bsky.bookmark.deleteBookmark'
    AppBskyBookmarkGetBookmarks: str = 'app.bsky.bookmark.getBookmarks'
    AppBskyContactDefs: str = 'app.bsky.contact.defs'
    AppBskyContactDismissMatch: str = 'app.bsky.contact.dismissMatch'
    AppBskyContactGetMatches: str = 'app.bsky.contact.getMatches'
    AppBskyContactGetSyncStatus: str = 'app.bsky.contact.getSyncStatus'
    AppBskyContactImportContacts: str = 'app.bsky.contact.importContacts'
    AppBskyContactRemoveData: str = 'app.bsky.contact.removeData'
    AppBskyContactStartPhoneVerification: str = 'app.bsky.contact.startPhoneVerification'
    AppBskyContactVerifyPhone: str = 'app.bsky.contact.verifyPhone'
    AppBskyEmbedDefs: str = 'app.bsky.embed.defs'
    AppBskyEmbedExternal: str = 'app.bsky.embed.external'
    AppBskyEmbedImages: str = 'app.bsky.embed.images'
    AppBskyEmbedRecord: str = 'app.bsky.embed.record'
    AppBskyEmbedRecordWithMedia: str = 'app.bsky.embed.recordWithMedia'
    AppBskyEmbedVideo: str = 'app.bsky.embed.video'
    AppBskyFeedDefs: str = 'app.bsky.feed.defs'
    AppBskyFeedDescribeFeedGenerator: str = 'app.bsky.feed.describeFeedGenerator'
    AppBskyFeedGenerator: str = 'app.bsky.feed.generator'
    AppBskyFeedGetActorFeeds: str = 'app.bsky.feed.getActorFeeds'
    AppBskyFeedGetActorLikes: str = 'app.bsky.feed.getActorLikes'
    AppBskyFeedGetAuthorFeed: str = 'app.bsky.feed.getAuthorFeed'
    AppBskyFeedGetFeed: str = 'app.bsky.feed.getFeed'
    AppBskyFeedGetFeedGenerator: str = 'app.bsky.feed.getFeedGenerator'
    AppBskyFeedGetFeedGenerators: str = 'app.bsky.feed.getFeedGenerators'
    AppBskyFeedGetFeedSkeleton: str = 'app.bsky.feed.getFeedSkeleton'
    AppBskyFeedGetLikes: str = 'app.bsky.feed.getLikes'
    AppBskyFeedGetListFeed: str = 'app.bsky.feed.getListFeed'
    AppBskyFeedGetPostThread: str = 'app.bsky.feed.getPostThread'
    AppBskyFeedGetPosts: str = 'app.bsky.feed.getPosts'
    AppBskyFeedGetQuotes: str = 'app.bsky.feed.getQuotes'
    AppBskyFeedGetRepostedBy: str = 'app.bsky.feed.getRepostedBy'
    AppBskyFeedGetSuggestedFeeds: str = 'app.bsky.feed.getSuggestedFeeds'
    AppBskyFeedGetTimeline: str = 'app.bsky.feed.getTimeline'
    AppBskyFeedLike: str = 'app.bsky.feed.like'
    AppBskyFeedPost: str = 'app.bsky.feed.post'
    AppBskyFeedPostgate: str = 'app.bsky.feed.postgate'
    AppBskyFeedRepost: str = 'app.bsky.feed.repost'
    AppBskyFeedSearchPosts: str = 'app.bsky.feed.searchPosts'
    AppBskyFeedSendInteractions: str = 'app.bsky.feed.sendInteractions'
    AppBskyFeedThreadgate: str = 'app.bsky.feed.threadgate'
    AppBskyGraphBlock: str = 'app.bsky.graph.block'
    AppBskyGraphDefs: str = 'app.bsky.graph.defs'
    AppBskyGraphFollow: str = 'app.bsky.graph.follow'
    AppBskyGraphGetActorStarterPacks: str = 'app.bsky.graph.getActorStarterPacks'
    AppBskyGraphGetBlocks: str = 'app.bsky.graph.getBlocks'
    AppBskyGraphGetFollowers: str = 'app.bsky.graph.getFollowers'
    AppBskyGraphGetFollows: str = 'app.bsky.graph.getFollows'
    AppBskyGraphGetKnownFollowers: str = 'app.bsky.graph.getKnownFollowers'
    AppBskyGraphGetList: str = 'app.bsky.graph.getList'
    AppBskyGraphGetListBlocks: str = 'app.bsky.graph.getListBlocks'
    AppBskyGraphGetListMutes: str = 'app.bsky.graph.getListMutes'
    AppBskyGraphGetLists: str = 'app.bsky.graph.getLists'
    AppBskyGraphGetListsWithMembership: str = 'app.bsky.graph.getListsWithMembership'
    AppBskyGraphGetMutes: str = 'app.bsky.graph.getMutes'
    AppBskyGraphGetRelationships: str = 'app.bsky.graph.getRelationships'
    AppBskyGraphGetStarterPack: str = 'app.bsky.graph.getStarterPack'
    AppBskyGraphGetStarterPacks: str = 'app.bsky.graph.getStarterPacks'
    AppBskyGraphGetStarterPacksWithMembership: str = 'app.bsky.graph.getStarterPacksWithMembership'
    AppBskyGraphGetSuggestedFollowsByActor: str = 'app.bsky.graph.getSuggestedFollowsByActor'
    AppBskyGraphList: str = 'app.bsky.graph.list'
    AppBskyGraphListblock: str = 'app.bsky.graph.listblock'
    AppBskyGraphListitem: str = 'app.bsky.graph.listitem'
    AppBskyGraphMuteActor: str = 'app.bsky.graph.muteActor'
    AppBskyGraphMuteActorList: str = 'app.bsky.graph.muteActorList'
    AppBskyGraphMuteThread: str = 'app.bsky.graph.muteThread'
    AppBskyGraphSearchStarterPacks: str = 'app.bsky.graph.searchStarterPacks'
    AppBskyGraphStarterpack: str = 'app.bsky.graph.starterpack'
    AppBskyGraphUnmuteActor: str = 'app.bsky.graph.unmuteActor'
    AppBskyGraphUnmuteActorList: str = 'app.bsky.graph.unmuteActorList'
    AppBskyGraphUnmuteThread: str = 'app.bsky.graph.unmuteThread'
    AppBskyGraphVerification: str = 'app.bsky.graph.verification'
    AppBskyLabelerDefs: str = 'app.bsky.labeler.defs'
    AppBskyLabelerGetServices: str = 'app.bsky.labeler.getServices'
    AppBskyLabelerService: str = 'app.bsky.labeler.service'
    AppBskyNotificationDeclaration: str = 'app.bsky.notification.declaration'
    AppBskyNotificationDefs: str = 'app.bsky.notification.defs'
    AppBskyNotificationGetPreferences: str = 'app.bsky.notification.getPreferences'
    AppBskyNotificationGetUnreadCount: str = 'app.bsky.notification.getUnreadCount'
    AppBskyNotificationListActivitySubscriptions: str = 'app.bsky.notification.listActivitySubscriptions'
    AppBskyNotificationListNotifications: str = 'app.bsky.notification.listNotifications'
    AppBskyNotificationPutActivitySubscription: str = 'app.bsky.notification.putActivitySubscription'
    AppBskyNotificationPutPreferences: str = 'app.bsky.notification.putPreferences'
    AppBskyNotificationPutPreferencesV2: str = 'app.bsky.notification.putPreferencesV2'
    AppBskyNotificationRegisterPush: str = 'app.bsky.notification.registerPush'
    AppBskyNotificationUnregisterPush: str = 'app.bsky.notification.unregisterPush'
    AppBskyNotificationUpdateSeen: str = 'app.bsky.notification.updateSeen'
    AppBskyRichtextFacet: str = 'app.bsky.richtext.facet'
    AppBskyUnspeccedDefs: str = 'app.bsky.unspecced.defs'
    AppBskyUnspeccedGetAgeAssuranceState: str = 'app.bsky.unspecced.getAgeAssuranceState'
    AppBskyUnspeccedGetConfig: str = 'app.bsky.unspecced.getConfig'
    AppBskyUnspeccedGetOnboardingSuggestedStarterPacks: str = 'app.bsky.unspecced.getOnboardingSuggestedStarterPacks'
    AppBskyUnspeccedGetOnboardingSuggestedStarterPacksSkeleton: str = (
        'app.bsky.unspecced.getOnboardingSuggestedStarterPacksSkeleton'
    )
    AppBskyUnspeccedGetPopularFeedGenerators: str = 'app.bsky.unspecced.getPopularFeedGenerators'
    AppBskyUnspeccedGetPostThreadOtherV2: str = 'app.bsky.unspecced.getPostThreadOtherV2'
    AppBskyUnspeccedGetPostThreadV2: str = 'app.bsky.unspecced.getPostThreadV2'
    AppBskyUnspeccedGetSuggestedFeeds: str = 'app.bsky.unspecced.getSuggestedFeeds'
    AppBskyUnspeccedGetSuggestedFeedsSkeleton: str = 'app.bsky.unspecced.getSuggestedFeedsSkeleton'
    AppBskyUnspeccedGetSuggestedStarterPacks: str = 'app.bsky.unspecced.getSuggestedStarterPacks'
    AppBskyUnspeccedGetSuggestedStarterPacksSkeleton: str = 'app.bsky.unspecced.getSuggestedStarterPacksSkeleton'
    AppBskyUnspeccedGetSuggestedUsers: str = 'app.bsky.unspecced.getSuggestedUsers'
    AppBskyUnspeccedGetSuggestedUsersSkeleton: str = 'app.bsky.unspecced.getSuggestedUsersSkeleton'
    AppBskyUnspeccedGetSuggestionsSkeleton: str = 'app.bsky.unspecced.getSuggestionsSkeleton'
    AppBskyUnspeccedGetTaggedSuggestions: str = 'app.bsky.unspecced.getTaggedSuggestions'
    AppBskyUnspeccedGetTrendingTopics: str = 'app.bsky.unspecced.getTrendingTopics'
    AppBskyUnspeccedGetTrends: str = 'app.bsky.unspecced.getTrends'
    AppBskyUnspeccedGetTrendsSkeleton: str = 'app.bsky.unspecced.getTrendsSkeleton'
    AppBskyUnspeccedInitAgeAssurance: str = 'app.bsky.unspecced.initAgeAssurance'
    AppBskyUnspeccedSearchActorsSkeleton: str = 'app.bsky.unspecced.searchActorsSkeleton'
    AppBskyUnspeccedSearchPostsSkeleton: str = 'app.bsky.unspecced.searchPostsSkeleton'
    AppBskyUnspeccedSearchStarterPacksSkeleton: str = 'app.bsky.unspecced.searchStarterPacksSkeleton'
    AppBskyVideoDefs: str = 'app.bsky.video.defs'
    AppBskyVideoGetJobStatus: str = 'app.bsky.video.getJobStatus'
    AppBskyVideoGetUploadLimits: str = 'app.bsky.video.getUploadLimits'
    AppBskyVideoUploadVideo: str = 'app.bsky.video.uploadVideo'
    ChatBskyActorDeclaration: str = 'chat.bsky.actor.declaration'
    ChatBskyActorDefs: str = 'chat.bsky.actor.defs'
    ChatBskyActorDeleteAccount: str = 'chat.bsky.actor.deleteAccount'
    ChatBskyActorExportAccountData: str = 'chat.bsky.actor.exportAccountData'
    ChatBskyConvoAcceptConvo: str = 'chat.bsky.convo.acceptConvo'
    ChatBskyConvoAddReaction: str = 'chat.bsky.convo.addReaction'
    ChatBskyConvoDefs: str = 'chat.bsky.convo.defs'
    ChatBskyConvoDeleteMessageForSelf: str = 'chat.bsky.convo.deleteMessageForSelf'
    ChatBskyConvoGetConvo: str = 'chat.bsky.convo.getConvo'
    ChatBskyConvoGetConvoAvailability: str = 'chat.bsky.convo.getConvoAvailability'
    ChatBskyConvoGetConvoForMembers: str = 'chat.bsky.convo.getConvoForMembers'
    ChatBskyConvoGetLog: str = 'chat.bsky.convo.getLog'
    ChatBskyConvoGetMessages: str = 'chat.bsky.convo.getMessages'
    ChatBskyConvoLeaveConvo: str = 'chat.bsky.convo.leaveConvo'
    ChatBskyConvoListConvos: str = 'chat.bsky.convo.listConvos'
    ChatBskyConvoMuteConvo: str = 'chat.bsky.convo.muteConvo'
    ChatBskyConvoRemoveReaction: str = 'chat.bsky.convo.removeReaction'
    ChatBskyConvoSendMessage: str = 'chat.bsky.convo.sendMessage'
    ChatBskyConvoSendMessageBatch: str = 'chat.bsky.convo.sendMessageBatch'
    ChatBskyConvoUnmuteConvo: str = 'chat.bsky.convo.unmuteConvo'
    ChatBskyConvoUpdateAllRead: str = 'chat.bsky.convo.updateAllRead'
    ChatBskyConvoUpdateRead: str = 'chat.bsky.convo.updateRead'
    ChatBskyModerationGetActorMetadata: str = 'chat.bsky.moderation.getActorMetadata'
    ChatBskyModerationGetMessageContext: str = 'chat.bsky.moderation.getMessageContext'
    ChatBskyModerationUpdateActorAccess: str = 'chat.bsky.moderation.updateActorAccess'
    ComAtprotoAdminDefs: str = 'com.atproto.admin.defs'
    ComAtprotoAdminDeleteAccount: str = 'com.atproto.admin.deleteAccount'
    ComAtprotoAdminDisableAccountInvites: str = 'com.atproto.admin.disableAccountInvites'
    ComAtprotoAdminDisableInviteCodes: str = 'com.atproto.admin.disableInviteCodes'
    ComAtprotoAdminEnableAccountInvites: str = 'com.atproto.admin.enableAccountInvites'
    ComAtprotoAdminGetAccountInfo: str = 'com.atproto.admin.getAccountInfo'
    ComAtprotoAdminGetAccountInfos: str = 'com.atproto.admin.getAccountInfos'
    ComAtprotoAdminGetInviteCodes: str = 'com.atproto.admin.getInviteCodes'
    ComAtprotoAdminGetSubjectStatus: str = 'com.atproto.admin.getSubjectStatus'
    ComAtprotoAdminSearchAccounts: str = 'com.atproto.admin.searchAccounts'
    ComAtprotoAdminSendEmail: str = 'com.atproto.admin.sendEmail'
    ComAtprotoAdminUpdateAccountEmail: str = 'com.atproto.admin.updateAccountEmail'
    ComAtprotoAdminUpdateAccountHandle: str = 'com.atproto.admin.updateAccountHandle'
    ComAtprotoAdminUpdateAccountPassword: str = 'com.atproto.admin.updateAccountPassword'
    ComAtprotoAdminUpdateAccountSigningKey: str = 'com.atproto.admin.updateAccountSigningKey'
    ComAtprotoAdminUpdateSubjectStatus: str = 'com.atproto.admin.updateSubjectStatus'
    ComAtprotoIdentityDefs: str = 'com.atproto.identity.defs'
    ComAtprotoIdentityGetRecommendedDidCredentials: str = 'com.atproto.identity.getRecommendedDidCredentials'
    ComAtprotoIdentityRefreshIdentity: str = 'com.atproto.identity.refreshIdentity'
    ComAtprotoIdentityRequestPlcOperationSignature: str = 'com.atproto.identity.requestPlcOperationSignature'
    ComAtprotoIdentityResolveDid: str = 'com.atproto.identity.resolveDid'
    ComAtprotoIdentityResolveHandle: str = 'com.atproto.identity.resolveHandle'
    ComAtprotoIdentityResolveIdentity: str = 'com.atproto.identity.resolveIdentity'
    ComAtprotoIdentitySignPlcOperation: str = 'com.atproto.identity.signPlcOperation'
    ComAtprotoIdentitySubmitPlcOperation: str = 'com.atproto.identity.submitPlcOperation'
    ComAtprotoIdentityUpdateHandle: str = 'com.atproto.identity.updateHandle'
    ComAtprotoLabelDefs: str = 'com.atproto.label.defs'
    ComAtprotoLabelQueryLabels: str = 'com.atproto.label.queryLabels'
    ComAtprotoLabelSubscribeLabels: str = 'com.atproto.label.subscribeLabels'
    ComAtprotoLexiconResolveLexicon: str = 'com.atproto.lexicon.resolveLexicon'
    ComAtprotoLexiconSchema: str = 'com.atproto.lexicon.schema'
    ComAtprotoModerationCreateReport: str = 'com.atproto.moderation.createReport'
    ComAtprotoModerationDefs: str = 'com.atproto.moderation.defs'
    ComAtprotoRepoApplyWrites: str = 'com.atproto.repo.applyWrites'
    ComAtprotoRepoCreateRecord: str = 'com.atproto.repo.createRecord'
    ComAtprotoRepoDefs: str = 'com.atproto.repo.defs'
    ComAtprotoRepoDeleteRecord: str = 'com.atproto.repo.deleteRecord'
    ComAtprotoRepoDescribeRepo: str = 'com.atproto.repo.describeRepo'
    ComAtprotoRepoGetRecord: str = 'com.atproto.repo.getRecord'
    ComAtprotoRepoImportRepo: str = 'com.atproto.repo.importRepo'
    ComAtprotoRepoListMissingBlobs: str = 'com.atproto.repo.listMissingBlobs'
    ComAtprotoRepoListRecords: str = 'com.atproto.repo.listRecords'
    ComAtprotoRepoPutRecord: str = 'com.atproto.repo.putRecord'
    ComAtprotoRepoStrongRef: str = 'com.atproto.repo.strongRef'
    ComAtprotoRepoUploadBlob: str = 'com.atproto.repo.uploadBlob'
    ComAtprotoServerActivateAccount: str = 'com.atproto.server.activateAccount'
    ComAtprotoServerCheckAccountStatus: str = 'com.atproto.server.checkAccountStatus'
    ComAtprotoServerConfirmEmail: str = 'com.atproto.server.confirmEmail'
    ComAtprotoServerCreateAccount: str = 'com.atproto.server.createAccount'
    ComAtprotoServerCreateAppPassword: str = 'com.atproto.server.createAppPassword'
    ComAtprotoServerCreateInviteCode: str = 'com.atproto.server.createInviteCode'
    ComAtprotoServerCreateInviteCodes: str = 'com.atproto.server.createInviteCodes'
    ComAtprotoServerCreateSession: str = 'com.atproto.server.createSession'
    ComAtprotoServerDeactivateAccount: str = 'com.atproto.server.deactivateAccount'
    ComAtprotoServerDefs: str = 'com.atproto.server.defs'
    ComAtprotoServerDeleteAccount: str = 'com.atproto.server.deleteAccount'
    ComAtprotoServerDeleteSession: str = 'com.atproto.server.deleteSession'
    ComAtprotoServerDescribeServer: str = 'com.atproto.server.describeServer'
    ComAtprotoServerGetAccountInviteCodes: str = 'com.atproto.server.getAccountInviteCodes'
    ComAtprotoServerGetServiceAuth: str = 'com.atproto.server.getServiceAuth'
    ComAtprotoServerGetSession: str = 'com.atproto.server.getSession'
    ComAtprotoServerListAppPasswords: str = 'com.atproto.server.listAppPasswords'
    ComAtprotoServerRefreshSession: str = 'com.atproto.server.refreshSession'
    ComAtprotoServerRequestAccountDelete: str = 'com.atproto.server.requestAccountDelete'
    ComAtprotoServerRequestEmailConfirmation: str = 'com.atproto.server.requestEmailConfirmation'
    ComAtprotoServerRequestEmailUpdate: str = 'com.atproto.server.requestEmailUpdate'
    ComAtprotoServerRequestPasswordReset: str = 'com.atproto.server.requestPasswordReset'
    ComAtprotoServerReserveSigningKey: str = 'com.atproto.server.reserveSigningKey'
    ComAtprotoServerResetPassword: str = 'com.atproto.server.resetPassword'
    ComAtprotoServerRevokeAppPassword: str = 'com.atproto.server.revokeAppPassword'
    ComAtprotoServerUpdateEmail: str = 'com.atproto.server.updateEmail'
    ComAtprotoSyncDefs: str = 'com.atproto.sync.defs'
    ComAtprotoSyncGetBlob: str = 'com.atproto.sync.getBlob'
    ComAtprotoSyncGetBlocks: str = 'com.atproto.sync.getBlocks'
    ComAtprotoSyncGetCheckout: str = 'com.atproto.sync.getCheckout'
    ComAtprotoSyncGetHead: str = 'com.atproto.sync.getHead'
    ComAtprotoSyncGetHostStatus: str = 'com.atproto.sync.getHostStatus'
    ComAtprotoSyncGetLatestCommit: str = 'com.atproto.sync.getLatestCommit'
    ComAtprotoSyncGetRecord: str = 'com.atproto.sync.getRecord'
    ComAtprotoSyncGetRepo: str = 'com.atproto.sync.getRepo'
    ComAtprotoSyncGetRepoStatus: str = 'com.atproto.sync.getRepoStatus'
    ComAtprotoSyncListBlobs: str = 'com.atproto.sync.listBlobs'
    ComAtprotoSyncListHosts: str = 'com.atproto.sync.listHosts'
    ComAtprotoSyncListRepos: str = 'com.atproto.sync.listRepos'
    ComAtprotoSyncListReposByCollection: str = 'com.atproto.sync.listReposByCollection'
    ComAtprotoSyncNotifyOfUpdate: str = 'com.atproto.sync.notifyOfUpdate'
    ComAtprotoSyncRequestCrawl: str = 'com.atproto.sync.requestCrawl'
    ComAtprotoSyncSubscribeRepos: str = 'com.atproto.sync.subscribeRepos'
    ComAtprotoTempAddReservedHandle: str = 'com.atproto.temp.addReservedHandle'
    ComAtprotoTempCheckHandleAvailability: str = 'com.atproto.temp.checkHandleAvailability'
    ComAtprotoTempCheckSignupQueue: str = 'com.atproto.temp.checkSignupQueue'
    ComAtprotoTempDereferenceScope: str = 'com.atproto.temp.dereferenceScope'
    ComAtprotoTempFetchLabels: str = 'com.atproto.temp.fetchLabels'
    ComAtprotoTempRequestPhoneVerification: str = 'com.atproto.temp.requestPhoneVerification'
    ComAtprotoTempRevokeAccountCredentials: str = 'com.atproto.temp.revokeAccountCredentials'
    ToolsOzoneCommunicationCreateTemplate: str = 'tools.ozone.communication.createTemplate'
    ToolsOzoneCommunicationDefs: str = 'tools.ozone.communication.defs'
    ToolsOzoneCommunicationDeleteTemplate: str = 'tools.ozone.communication.deleteTemplate'
    ToolsOzoneCommunicationListTemplates: str = 'tools.ozone.communication.listTemplates'
    ToolsOzoneCommunicationUpdateTemplate: str = 'tools.ozone.communication.updateTemplate'
    ToolsOzoneHostingGetAccountHistory: str = 'tools.ozone.hosting.getAccountHistory'
    ToolsOzoneModerationCancelScheduledActions: str = 'tools.ozone.moderation.cancelScheduledActions'
    ToolsOzoneModerationDefs: str = 'tools.ozone.moderation.defs'
    ToolsOzoneModerationEmitEvent: str = 'tools.ozone.moderation.emitEvent'
    ToolsOzoneModerationGetAccountTimeline: str = 'tools.ozone.moderation.getAccountTimeline'
    ToolsOzoneModerationGetEvent: str = 'tools.ozone.moderation.getEvent'
    ToolsOzoneModerationGetRecord: str = 'tools.ozone.moderation.getRecord'
    ToolsOzoneModerationGetRecords: str = 'tools.ozone.moderation.getRecords'
    ToolsOzoneModerationGetRepo: str = 'tools.ozone.moderation.getRepo'
    ToolsOzoneModerationGetReporterStats: str = 'tools.ozone.moderation.getReporterStats'
    ToolsOzoneModerationGetRepos: str = 'tools.ozone.moderation.getRepos'
    ToolsOzoneModerationGetSubjects: str = 'tools.ozone.moderation.getSubjects'
    ToolsOzoneModerationListScheduledActions: str = 'tools.ozone.moderation.listScheduledActions'
    ToolsOzoneModerationQueryEvents: str = 'tools.ozone.moderation.queryEvents'
    ToolsOzoneModerationQueryStatuses: str = 'tools.ozone.moderation.queryStatuses'
    ToolsOzoneModerationScheduleAction: str = 'tools.ozone.moderation.scheduleAction'
    ToolsOzoneModerationSearchRepos: str = 'tools.ozone.moderation.searchRepos'
    ToolsOzoneReportDefs: str = 'tools.ozone.report.defs'
    ToolsOzoneSafelinkAddRule: str = 'tools.ozone.safelink.addRule'
    ToolsOzoneSafelinkDefs: str = 'tools.ozone.safelink.defs'
    ToolsOzoneSafelinkQueryEvents: str = 'tools.ozone.safelink.queryEvents'
    ToolsOzoneSafelinkQueryRules: str = 'tools.ozone.safelink.queryRules'
    ToolsOzoneSafelinkRemoveRule: str = 'tools.ozone.safelink.removeRule'
    ToolsOzoneSafelinkUpdateRule: str = 'tools.ozone.safelink.updateRule'
    ToolsOzoneServerGetConfig: str = 'tools.ozone.server.getConfig'
    ToolsOzoneSetAddValues: str = 'tools.ozone.set.addValues'
    ToolsOzoneSetDefs: str = 'tools.ozone.set.defs'
    ToolsOzoneSetDeleteSet: str = 'tools.ozone.set.deleteSet'
    ToolsOzoneSetDeleteValues: str = 'tools.ozone.set.deleteValues'
    ToolsOzoneSetGetValues: str = 'tools.ozone.set.getValues'
    ToolsOzoneSetQuerySets: str = 'tools.ozone.set.querySets'
    ToolsOzoneSetUpsertSet: str = 'tools.ozone.set.upsertSet'
    ToolsOzoneSettingDefs: str = 'tools.ozone.setting.defs'
    ToolsOzoneSettingListOptions: str = 'tools.ozone.setting.listOptions'
    ToolsOzoneSettingRemoveOptions: str = 'tools.ozone.setting.removeOptions'
    ToolsOzoneSettingUpsertOption: str = 'tools.ozone.setting.upsertOption'
    ToolsOzoneSignatureDefs: str = 'tools.ozone.signature.defs'
    ToolsOzoneSignatureFindCorrelation: str = 'tools.ozone.signature.findCorrelation'
    ToolsOzoneSignatureFindRelatedAccounts: str = 'tools.ozone.signature.findRelatedAccounts'
    ToolsOzoneSignatureSearchAccounts: str = 'tools.ozone.signature.searchAccounts'
    ToolsOzoneTeamAddMember: str = 'tools.ozone.team.addMember'
    ToolsOzoneTeamDefs: str = 'tools.ozone.team.defs'
    ToolsOzoneTeamDeleteMember: str = 'tools.ozone.team.deleteMember'
    ToolsOzoneTeamListMembers: str = 'tools.ozone.team.listMembers'
    ToolsOzoneTeamUpdateMember: str = 'tools.ozone.team.updateMember'
    ToolsOzoneVerificationDefs: str = 'tools.ozone.verification.defs'
    ToolsOzoneVerificationGrantVerifications: str = 'tools.ozone.verification.grantVerifications'
    ToolsOzoneVerificationListVerifications: str = 'tools.ozone.verification.listVerifications'
    ToolsOzoneVerificationRevokeVerifications: str = 'tools.ozone.verification.revokeVerifications'


ids = _Ids()
load_models()
