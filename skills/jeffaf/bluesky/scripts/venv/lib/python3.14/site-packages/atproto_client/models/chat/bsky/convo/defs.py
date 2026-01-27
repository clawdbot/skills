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


class MessageRef(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    convo_id: str  #: Convo id.
    did: string_formats.Did  #: Did.
    message_id: str  #: Message id.

    py_type: t.Literal['chat.bsky.convo.defs#messageRef'] = Field(
        default='chat.bsky.convo.defs#messageRef', alias='$type', frozen=True
    )


class MessageInput(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    text: str = Field(max_length=10000)  #: Text.
    embed: t.Optional[te.Annotated[t.Union['models.AppBskyEmbedRecord.Main'], Field(discriminator='py_type')]] = (
        None  #: Embed.
    )
    facets: t.Optional[t.List['models.AppBskyRichtextFacet.Main']] = (
        None  #: Annotations of text (mentions, URLs, hashtags, etc).
    )

    py_type: t.Literal['chat.bsky.convo.defs#messageInput'] = Field(
        default='chat.bsky.convo.defs#messageInput', alias='$type', frozen=True
    )


class MessageView(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    id: str  #: Id.
    rev: str  #: Rev.
    sender: 'models.ChatBskyConvoDefs.MessageViewSender'  #: Sender.
    sent_at: string_formats.DateTime  #: Sent at.
    text: str = Field(max_length=10000)  #: Text.
    embed: t.Optional[te.Annotated[t.Union['models.AppBskyEmbedRecord.View'], Field(discriminator='py_type')]] = (
        None  #: Embed.
    )
    facets: t.Optional[t.List['models.AppBskyRichtextFacet.Main']] = (
        None  #: Annotations of text (mentions, URLs, hashtags, etc).
    )
    reactions: t.Optional[t.List['models.ChatBskyConvoDefs.ReactionView']] = (
        None  #: Reactions to this message, in ascending order of creation time.
    )

    py_type: t.Literal['chat.bsky.convo.defs#messageView'] = Field(
        default='chat.bsky.convo.defs#messageView', alias='$type', frozen=True
    )


class DeletedMessageView(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    id: str  #: Id.
    rev: str  #: Rev.
    sender: 'models.ChatBskyConvoDefs.MessageViewSender'  #: Sender.
    sent_at: string_formats.DateTime  #: Sent at.

    py_type: t.Literal['chat.bsky.convo.defs#deletedMessageView'] = Field(
        default='chat.bsky.convo.defs#deletedMessageView', alias='$type', frozen=True
    )


class MessageViewSender(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    did: string_formats.Did  #: Did.

    py_type: t.Literal['chat.bsky.convo.defs#messageViewSender'] = Field(
        default='chat.bsky.convo.defs#messageViewSender', alias='$type', frozen=True
    )


class ReactionView(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    created_at: string_formats.DateTime  #: Created at.
    sender: 'models.ChatBskyConvoDefs.ReactionViewSender'  #: Sender.
    value: str  #: Value.

    py_type: t.Literal['chat.bsky.convo.defs#reactionView'] = Field(
        default='chat.bsky.convo.defs#reactionView', alias='$type', frozen=True
    )


class ReactionViewSender(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    did: string_formats.Did  #: Did.

    py_type: t.Literal['chat.bsky.convo.defs#reactionViewSender'] = Field(
        default='chat.bsky.convo.defs#reactionViewSender', alias='$type', frozen=True
    )


class MessageAndReactionView(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    message: 'models.ChatBskyConvoDefs.MessageView'  #: Message.
    reaction: 'models.ChatBskyConvoDefs.ReactionView'  #: Reaction.

    py_type: t.Literal['chat.bsky.convo.defs#messageAndReactionView'] = Field(
        default='chat.bsky.convo.defs#messageAndReactionView', alias='$type', frozen=True
    )


class ConvoView(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    id: str  #: Id.
    members: t.List['models.ChatBskyActorDefs.ProfileViewBasic']  #: Members.
    muted: bool  #: Muted.
    rev: str  #: Rev.
    unread_count: int  #: Unread count.
    last_message: t.Optional[
        te.Annotated[
            t.Union['models.ChatBskyConvoDefs.MessageView', 'models.ChatBskyConvoDefs.DeletedMessageView'],
            Field(discriminator='py_type'),
        ]
    ] = None  #: Last message.
    last_reaction: t.Optional[
        te.Annotated[t.Union['models.ChatBskyConvoDefs.MessageAndReactionView'], Field(discriminator='py_type')]
    ] = None  #: Last reaction.
    status: t.Optional[t.Union[t.Literal['request'], t.Literal['accepted'], str]] = None  #: Status.

    py_type: t.Literal['chat.bsky.convo.defs#convoView'] = Field(
        default='chat.bsky.convo.defs#convoView', alias='$type', frozen=True
    )


class LogBeginConvo(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    convo_id: str  #: Convo id.
    rev: str  #: Rev.

    py_type: t.Literal['chat.bsky.convo.defs#logBeginConvo'] = Field(
        default='chat.bsky.convo.defs#logBeginConvo', alias='$type', frozen=True
    )


class LogAcceptConvo(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    convo_id: str  #: Convo id.
    rev: str  #: Rev.

    py_type: t.Literal['chat.bsky.convo.defs#logAcceptConvo'] = Field(
        default='chat.bsky.convo.defs#logAcceptConvo', alias='$type', frozen=True
    )


class LogLeaveConvo(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    convo_id: str  #: Convo id.
    rev: str  #: Rev.

    py_type: t.Literal['chat.bsky.convo.defs#logLeaveConvo'] = Field(
        default='chat.bsky.convo.defs#logLeaveConvo', alias='$type', frozen=True
    )


class LogMuteConvo(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    convo_id: str  #: Convo id.
    rev: str  #: Rev.

    py_type: t.Literal['chat.bsky.convo.defs#logMuteConvo'] = Field(
        default='chat.bsky.convo.defs#logMuteConvo', alias='$type', frozen=True
    )


class LogUnmuteConvo(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    convo_id: str  #: Convo id.
    rev: str  #: Rev.

    py_type: t.Literal['chat.bsky.convo.defs#logUnmuteConvo'] = Field(
        default='chat.bsky.convo.defs#logUnmuteConvo', alias='$type', frozen=True
    )


class LogCreateMessage(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    convo_id: str  #: Convo id.
    message: te.Annotated[
        t.Union['models.ChatBskyConvoDefs.MessageView', 'models.ChatBskyConvoDefs.DeletedMessageView'],
        Field(discriminator='py_type'),
    ]  #: Message.
    rev: str  #: Rev.

    py_type: t.Literal['chat.bsky.convo.defs#logCreateMessage'] = Field(
        default='chat.bsky.convo.defs#logCreateMessage', alias='$type', frozen=True
    )


class LogDeleteMessage(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    convo_id: str  #: Convo id.
    message: te.Annotated[
        t.Union['models.ChatBskyConvoDefs.MessageView', 'models.ChatBskyConvoDefs.DeletedMessageView'],
        Field(discriminator='py_type'),
    ]  #: Message.
    rev: str  #: Rev.

    py_type: t.Literal['chat.bsky.convo.defs#logDeleteMessage'] = Field(
        default='chat.bsky.convo.defs#logDeleteMessage', alias='$type', frozen=True
    )


class LogReadMessage(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    convo_id: str  #: Convo id.
    message: te.Annotated[
        t.Union['models.ChatBskyConvoDefs.MessageView', 'models.ChatBskyConvoDefs.DeletedMessageView'],
        Field(discriminator='py_type'),
    ]  #: Message.
    rev: str  #: Rev.

    py_type: t.Literal['chat.bsky.convo.defs#logReadMessage'] = Field(
        default='chat.bsky.convo.defs#logReadMessage', alias='$type', frozen=True
    )


class LogAddReaction(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    convo_id: str  #: Convo id.
    message: te.Annotated[
        t.Union['models.ChatBskyConvoDefs.MessageView', 'models.ChatBskyConvoDefs.DeletedMessageView'],
        Field(discriminator='py_type'),
    ]  #: Message.
    reaction: 'models.ChatBskyConvoDefs.ReactionView'  #: Reaction.
    rev: str  #: Rev.

    py_type: t.Literal['chat.bsky.convo.defs#logAddReaction'] = Field(
        default='chat.bsky.convo.defs#logAddReaction', alias='$type', frozen=True
    )


class LogRemoveReaction(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.defs`."""

    convo_id: str  #: Convo id.
    message: te.Annotated[
        t.Union['models.ChatBskyConvoDefs.MessageView', 'models.ChatBskyConvoDefs.DeletedMessageView'],
        Field(discriminator='py_type'),
    ]  #: Message.
    reaction: 'models.ChatBskyConvoDefs.ReactionView'  #: Reaction.
    rev: str  #: Rev.

    py_type: t.Literal['chat.bsky.convo.defs#logRemoveReaction'] = Field(
        default='chat.bsky.convo.defs#logRemoveReaction', alias='$type', frozen=True
    )
