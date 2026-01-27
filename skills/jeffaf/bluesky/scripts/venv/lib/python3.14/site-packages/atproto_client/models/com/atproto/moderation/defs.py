##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

if t.TYPE_CHECKING:
    from atproto_client import models

ReasonType = t.Union[
    'models.ComAtprotoModerationDefs.ReasonSpam',
    'models.ComAtprotoModerationDefs.ReasonViolation',
    'models.ComAtprotoModerationDefs.ReasonMisleading',
    'models.ComAtprotoModerationDefs.ReasonSexual',
    'models.ComAtprotoModerationDefs.ReasonRude',
    'models.ComAtprotoModerationDefs.ReasonOther',
    'models.ComAtprotoModerationDefs.ReasonAppeal',
    'models.ToolsOzoneReportDefs.ReasonAppeal',
    'models.ToolsOzoneReportDefs.ReasonOther',
    'models.ToolsOzoneReportDefs.ReasonViolenceAnimal',
    'models.ToolsOzoneReportDefs.ReasonViolenceThreats',
    'models.ToolsOzoneReportDefs.ReasonViolenceGraphicContent',
    'models.ToolsOzoneReportDefs.ReasonViolenceGlorification',
    'models.ToolsOzoneReportDefs.ReasonViolenceExtremistContent',
    'models.ToolsOzoneReportDefs.ReasonViolenceTrafficking',
    'models.ToolsOzoneReportDefs.ReasonViolenceOther',
    'models.ToolsOzoneReportDefs.ReasonSexualAbuseContent',
    'models.ToolsOzoneReportDefs.ReasonSexualNCII',
    'models.ToolsOzoneReportDefs.ReasonSexualDeepfake',
    'models.ToolsOzoneReportDefs.ReasonSexualAnimal',
    'models.ToolsOzoneReportDefs.ReasonSexualUnlabeled',
    'models.ToolsOzoneReportDefs.ReasonSexualOther',
    'models.ToolsOzoneReportDefs.ReasonChildSafetyCSAM',
    'models.ToolsOzoneReportDefs.ReasonChildSafetyGroom',
    'models.ToolsOzoneReportDefs.ReasonChildSafetyPrivacy',
    'models.ToolsOzoneReportDefs.ReasonChildSafetyHarassment',
    'models.ToolsOzoneReportDefs.ReasonChildSafetyOther',
    'models.ToolsOzoneReportDefs.ReasonHarassmentTroll',
    'models.ToolsOzoneReportDefs.ReasonHarassmentTargeted',
    'models.ToolsOzoneReportDefs.ReasonHarassmentHateSpeech',
    'models.ToolsOzoneReportDefs.ReasonHarassmentDoxxing',
    'models.ToolsOzoneReportDefs.ReasonHarassmentOther',
    'models.ToolsOzoneReportDefs.ReasonMisleadingBot',
    'models.ToolsOzoneReportDefs.ReasonMisleadingImpersonation',
    'models.ToolsOzoneReportDefs.ReasonMisleadingSpam',
    'models.ToolsOzoneReportDefs.ReasonMisleadingScam',
    'models.ToolsOzoneReportDefs.ReasonMisleadingElections',
    'models.ToolsOzoneReportDefs.ReasonMisleadingOther',
    'models.ToolsOzoneReportDefs.ReasonRuleSiteSecurity',
    'models.ToolsOzoneReportDefs.ReasonRuleProhibitedSales',
    'models.ToolsOzoneReportDefs.ReasonRuleBanEvasion',
    'models.ToolsOzoneReportDefs.ReasonRuleOther',
    'models.ToolsOzoneReportDefs.ReasonSelfHarmContent',
    'models.ToolsOzoneReportDefs.ReasonSelfHarmED',
    'models.ToolsOzoneReportDefs.ReasonSelfHarmStunts',
    'models.ToolsOzoneReportDefs.ReasonSelfHarmSubstances',
    'models.ToolsOzoneReportDefs.ReasonSelfHarmOther',
    str,
]  #: Reason type

ReasonSpam = t.Literal[
    'com.atproto.moderation.defs#reasonSpam'
]  #: Spam: frequent unwanted promotion, replies, mentions. Prefer new lexicon definition `tools.ozone.report.defs#reasonMisleadingSpam`.

ReasonViolation = t.Literal[
    'com.atproto.moderation.defs#reasonViolation'
]  #: Direct violation of server rules, laws, terms of service. Prefer new lexicon definition `tools.ozone.report.defs#reasonRuleOther`.

ReasonMisleading = t.Literal[
    'com.atproto.moderation.defs#reasonMisleading'
]  #: Misleading identity, affiliation, or content. Prefer new lexicon definition `tools.ozone.report.defs#reasonMisleadingOther`.

ReasonSexual = t.Literal[
    'com.atproto.moderation.defs#reasonSexual'
]  #: Unwanted or mislabeled sexual content. Prefer new lexicon definition `tools.ozone.report.defs#reasonSexualUnlabeled`.

ReasonRude = t.Literal[
    'com.atproto.moderation.defs#reasonRude'
]  #: Rude, harassing, explicit, or otherwise unwelcoming behavior. Prefer new lexicon definition `tools.ozone.report.defs#reasonHarassmentOther`.

ReasonOther = t.Literal[
    'com.atproto.moderation.defs#reasonOther'
]  #: Reports not falling under another report category. Prefer new lexicon definition `tools.ozone.report.defs#reasonOther`.

ReasonAppeal = t.Literal['com.atproto.moderation.defs#reasonAppeal']  #: Appeal a previously taken moderation action

SubjectType = t.Union[
    t.Literal['account'], t.Literal['record'], t.Literal['chat'], str
]  #: Tag describing a type of subject that might be reported.
