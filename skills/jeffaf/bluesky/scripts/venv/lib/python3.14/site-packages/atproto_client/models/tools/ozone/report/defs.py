##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

if t.TYPE_CHECKING:
    from atproto_client import models

ReasonType = t.Union[
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

ReasonAppeal = t.Literal['tools.ozone.report.defs#reasonAppeal']  #: Appeal a previously taken moderation action

ReasonOther = t.Literal['tools.ozone.report.defs#reasonOther']  #: An issue not included in these options

ReasonViolenceAnimal = t.Literal['tools.ozone.report.defs#reasonViolenceAnimal']  #: Animal welfare violations

ReasonViolenceThreats = t.Literal['tools.ozone.report.defs#reasonViolenceThreats']  #: Threats or incitement

ReasonViolenceGraphicContent = t.Literal[
    'tools.ozone.report.defs#reasonViolenceGraphicContent'
]  #: Graphic violent content

ReasonViolenceGlorification = t.Literal[
    'tools.ozone.report.defs#reasonViolenceGlorification'
]  #: Glorification of violence

ReasonViolenceExtremistContent = t.Literal[
    'tools.ozone.report.defs#reasonViolenceExtremistContent'
]  #: Extremist content. These reports will be sent only be sent to the application's Moderation Authority.

ReasonViolenceTrafficking = t.Literal['tools.ozone.report.defs#reasonViolenceTrafficking']  #: Human trafficking

ReasonViolenceOther = t.Literal['tools.ozone.report.defs#reasonViolenceOther']  #: Other violent content

ReasonSexualAbuseContent = t.Literal['tools.ozone.report.defs#reasonSexualAbuseContent']  #: Adult sexual abuse content

ReasonSexualNCII = t.Literal['tools.ozone.report.defs#reasonSexualNCII']  #: Non-consensual intimate imagery

ReasonSexualDeepfake = t.Literal['tools.ozone.report.defs#reasonSexualDeepfake']  #: Deepfake adult content

ReasonSexualAnimal = t.Literal['tools.ozone.report.defs#reasonSexualAnimal']  #: Animal sexual abuse

ReasonSexualUnlabeled = t.Literal['tools.ozone.report.defs#reasonSexualUnlabeled']  #: Unlabelled adult content

ReasonSexualOther = t.Literal['tools.ozone.report.defs#reasonSexualOther']  #: Other sexual violence content

ReasonChildSafetyCSAM = t.Literal[
    'tools.ozone.report.defs#reasonChildSafetyCSAM'
]  #: Child sexual abuse material (CSAM). These reports will be sent only be sent to the application's Moderation Authority.

ReasonChildSafetyGroom = t.Literal[
    'tools.ozone.report.defs#reasonChildSafetyGroom'
]  #: Grooming or predatory behavior. These reports will be sent only be sent to the application's Moderation Authority.

ReasonChildSafetyPrivacy = t.Literal[
    'tools.ozone.report.defs#reasonChildSafetyPrivacy'
]  #: Privacy violation involving a minor

ReasonChildSafetyHarassment = t.Literal[
    'tools.ozone.report.defs#reasonChildSafetyHarassment'
]  #: Harassment or bullying of minors

ReasonChildSafetyOther = t.Literal[
    'tools.ozone.report.defs#reasonChildSafetyOther'
]  #: Other child safety. These reports will be sent only be sent to the application's Moderation Authority.

ReasonHarassmentTroll = t.Literal['tools.ozone.report.defs#reasonHarassmentTroll']  #: Trolling

ReasonHarassmentTargeted = t.Literal['tools.ozone.report.defs#reasonHarassmentTargeted']  #: Targeted harassment

ReasonHarassmentHateSpeech = t.Literal['tools.ozone.report.defs#reasonHarassmentHateSpeech']  #: Hate speech

ReasonHarassmentDoxxing = t.Literal['tools.ozone.report.defs#reasonHarassmentDoxxing']  #: Doxxing

ReasonHarassmentOther = t.Literal[
    'tools.ozone.report.defs#reasonHarassmentOther'
]  #: Other harassing or hateful content

ReasonMisleadingBot = t.Literal['tools.ozone.report.defs#reasonMisleadingBot']  #: Fake account or bot

ReasonMisleadingImpersonation = t.Literal['tools.ozone.report.defs#reasonMisleadingImpersonation']  #: Impersonation

ReasonMisleadingSpam = t.Literal['tools.ozone.report.defs#reasonMisleadingSpam']  #: Spam

ReasonMisleadingScam = t.Literal['tools.ozone.report.defs#reasonMisleadingScam']  #: Scam

ReasonMisleadingElections = t.Literal[
    'tools.ozone.report.defs#reasonMisleadingElections'
]  #: False information about elections

ReasonMisleadingOther = t.Literal['tools.ozone.report.defs#reasonMisleadingOther']  #: Other misleading content

ReasonRuleSiteSecurity = t.Literal['tools.ozone.report.defs#reasonRuleSiteSecurity']  #: Hacking or system attacks

ReasonRuleProhibitedSales = t.Literal[
    'tools.ozone.report.defs#reasonRuleProhibitedSales'
]  #: Promoting or selling prohibited items or services

ReasonRuleBanEvasion = t.Literal['tools.ozone.report.defs#reasonRuleBanEvasion']  #: Banned user returning

ReasonRuleOther = t.Literal['tools.ozone.report.defs#reasonRuleOther']  #: Other

ReasonSelfHarmContent = t.Literal[
    'tools.ozone.report.defs#reasonSelfHarmContent'
]  #: Content promoting or depicting self-harm

ReasonSelfHarmED = t.Literal['tools.ozone.report.defs#reasonSelfHarmED']  #: Eating disorders

ReasonSelfHarmStunts = t.Literal['tools.ozone.report.defs#reasonSelfHarmStunts']  #: Dangerous challenges or activities

ReasonSelfHarmSubstances = t.Literal[
    'tools.ozone.report.defs#reasonSelfHarmSubstances'
]  #: Dangerous substances or drug abuse

ReasonSelfHarmOther = t.Literal['tools.ozone.report.defs#reasonSelfHarmOther']  #: Other dangerous content
