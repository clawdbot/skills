import typing as t
from threading import Lock

from atproto_core.uri import AtUri

from atproto_client import models
from atproto_client.client.methods_mixin import SessionMethodsMixin, TimeMethodsMixin
from atproto_client.client.methods_mixin.headers import HeadersConfigurationMethodsMixin
from atproto_client.client.methods_mixin.session import SessionDispatchMixin
from atproto_client.client.raw import ClientRaw
from atproto_client.client.session import Session, SessionEvent, SessionResponse
from atproto_client.exceptions import LoginRequiredError
from atproto_client.models.languages import DEFAULT_LANGUAGE_CODE1
from atproto_client.utils import TextBuilder

if t.TYPE_CHECKING:
    from atproto_client.client.base import InvokeType
    from atproto_client.request import Response


class Client(SessionDispatchMixin, SessionMethodsMixin, TimeMethodsMixin, HeadersConfigurationMethodsMixin, ClientRaw):
    """High-level client for XRPC of ATProto."""

    def __init__(self, base_url: t.Optional[str] = None, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(base_url, *args, **kwargs)

        self._refresh_lock = Lock()

        self.me: t.Optional['models.AppBskyActorDefs.ProfileViewDetailed'] = None

    def _invoke(self, invoke_type: 'InvokeType', **kwargs: t.Any) -> 'Response':
        ignore_session_check = kwargs.pop('ignore_session_check', False)
        if ignore_session_check:
            return super()._invoke(invoke_type, **kwargs)

        with self._refresh_lock:
            if self._session and self._session.access_jwt and self._should_refresh_session():
                self._refresh_and_set_session()

        return super()._invoke(invoke_type, **kwargs)

    def _set_session(self, event: SessionEvent, session: SessionResponse) -> None:
        self._set_session_common(session, self._base_url)
        self._call_on_session_change_callbacks(event)

    def _get_and_set_session(
        self, login: str, password: str, auth_factor_token: t.Optional[str] = None
    ) -> 'models.ComAtprotoServerCreateSession.Response':
        session = self.com.atproto.server.create_session(
            models.ComAtprotoServerCreateSession.Data(
                identifier=login, password=password, auth_factor_token=auth_factor_token
            ),
            ignore_session_check=True,
        )
        self._set_session(SessionEvent.CREATE, session)
        return session

    def _refresh_and_set_session(self) -> 'models.ComAtprotoServerRefreshSession.Response':
        if not self._session or not self._session.refresh_jwt:
            raise LoginRequiredError

        refresh_session = self.com.atproto.server.refresh_session(
            headers=self._get_refresh_auth_headers(), ignore_session_check=True
        )
        self._set_session(SessionEvent.REFRESH, refresh_session)

        return refresh_session

    def _import_session_string(self, session_string: str) -> Session:
        import_session = Session.decode(session_string)
        self._set_session(SessionEvent.IMPORT, import_session)

        return import_session

    def login(
        self,
        login: t.Optional[str] = None,
        password: t.Optional[str] = None,
        session_string: t.Optional[str] = None,
        auth_factor_token: t.Optional[str] = None,
    ) -> 'models.AppBskyActorDefs.ProfileViewDetailed':
        """Authorize a client and get profile info.

        Args:
            login: Handle/username of the account.
            password: Main or app-specific password of the account.
            session_string: Session string (use :py:attr:`~export_session_string` to get it).
            auth_factor_token: Auth factor token (for Email 2FA).

        Note:
            Either `session_string` or `login` and `password` should be provided.

        Returns:
            :obj:`models.AppBskyActorDefs.ProfileViewDetailed`: Profile information.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        if session_string:
            session = self._import_session_string(session_string)
        elif login and password:
            session = self._get_and_set_session(login, password, auth_factor_token)
        else:
            raise ValueError('Either session_string or login and password should be provided.')

        self.me = self.app.bsky.actor.get_profile(models.AppBskyActorGetProfile.Params(actor=session.handle))
        return self.me

    def send_post(
        self,
        text: t.Union[str, TextBuilder],
        profile_identify: t.Optional[str] = None,
        reply_to: t.Optional['models.AppBskyFeedPost.ReplyRef'] = None,
        embed: t.Optional[
            t.Union[
                'models.AppBskyEmbedImages.Main',
                'models.AppBskyEmbedExternal.Main',
                'models.AppBskyEmbedRecord.Main',
                'models.AppBskyEmbedRecordWithMedia.Main',
                'models.AppBskyEmbedVideo.Main',
            ]
        ] = None,
        langs: t.Optional[t.List[str]] = None,
        facets: t.Optional[t.List['models.AppBskyRichtextFacet.Main']] = None,
    ) -> 'models.AppBskyFeedPost.CreateRecordResponse':
        """Send post.

        Note:
            If `profile_identify` is not provided will be sent to the current profile.

            The default language is ``en``.
            Available languages are defined in :py:mod:`atproto.xrpc_client.models.languages`.

        Args:
            text: Text of the post.
            profile_identify: Handle or DID. Where to send post.
            reply_to: Root and parent of the post to reply to.
            embed: Embed models that should be attached to the post.
            langs: List of used languages in the post.
            facets: List of facets (rich text items).

        Returns:
            :obj:`models.AppBskyFeedPost.CreateRecordResponse`: Reference to the created record.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        if isinstance(text, TextBuilder):
            facets = text.build_facets()
            text = text.build_text()

        repo = self.me and self.me.did
        if profile_identify:
            repo = profile_identify

        if not repo:
            raise LoginRequiredError

        if not langs:
            langs = [DEFAULT_LANGUAGE_CODE1]

        record = models.AppBskyFeedPost.Record(
            created_at=self.get_current_time_iso(),
            text=text,
            reply=reply_to,
            embed=embed,
            langs=langs,
            facets=facets,
        )
        return self.app.bsky.feed.post.create(repo, record)

    def delete_post(self, post_uri: str) -> bool:
        """Delete post.

        Args:
            post_uri: AT URI of the post.

        Returns:
            :obj:`bool`: Success status.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        uri = AtUri.from_str(post_uri)
        return self.app.bsky.feed.post.delete(uri.hostname, uri.rkey)

    def send_images(
        self,
        text: t.Union[str, TextBuilder],
        images: t.List[bytes],
        image_alts: t.Optional[t.List[str]] = None,
        profile_identify: t.Optional[str] = None,
        reply_to: t.Optional['models.AppBskyFeedPost.ReplyRef'] = None,
        langs: t.Optional[t.List[str]] = None,
        facets: t.Optional[t.List['models.AppBskyRichtextFacet.Main']] = None,
        image_aspect_ratios: t.Optional[t.List['models.AppBskyEmbedDefs.AspectRatio']] = None,
    ) -> 'models.AppBskyFeedPost.CreateRecordResponse':
        """Send post with multiple attached images (up to 4 images).

        Note:
            If `profile_identify` is not provided will be sent to the current profile.

        Args:
            text: Text of the post.
            images: List of binary images to attach. The length must be less than or equal to 4.
            image_alts: List of text version of the images.
                        The length should be shorter than or equal to the length of `images`.
            profile_identify: Handle or DID. Where to send post.
            reply_to: Root and parent of the post to reply to.
            langs: List of used languages in the post.
            facets: List of facets (rich text items).
            image_aspect_ratios: List of aspect ratios of the images.
                        The length should be shorter than or equal to the length of `images`.

        Returns:
            :obj:`models.AppBskyFeedPost.CreateRecordResponse`: Reference to the created record.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        if image_alts is None:
            image_alts = [''] * len(images)
        else:
            # padding with empty string if len is insufficient
            diff = len(images) - len(image_alts)
            image_alts = image_alts + [''] * diff  # [''] * (minus) => []

        if image_aspect_ratios is None:
            aligned_image_aspect_ratios = [None] * len(images)
        else:
            # padding with None if len is insufficient
            diff = len(images) - len(image_aspect_ratios)
            aligned_image_aspect_ratios = image_aspect_ratios + [None] * diff

        uploads = [self.upload_blob(image) for image in images]
        embed_images = [
            models.AppBskyEmbedImages.Image(alt=alt, image=upload.blob, aspect_ratio=aspect_ratio)
            for alt, upload, aspect_ratio in zip(image_alts, uploads, aligned_image_aspect_ratios)
        ]

        return self.send_post(
            text,
            profile_identify=profile_identify,
            reply_to=reply_to,
            embed=models.AppBskyEmbedImages.Main(images=embed_images),
            langs=langs,
            facets=facets,
        )

    def send_image(
        self,
        text: t.Union[str, TextBuilder],
        image: bytes,
        image_alt: str,
        profile_identify: t.Optional[str] = None,
        reply_to: t.Optional['models.AppBskyFeedPost.ReplyRef'] = None,
        langs: t.Optional[t.List[str]] = None,
        facets: t.Optional[t.List['models.AppBskyRichtextFacet.Main']] = None,
        image_aspect_ratio: t.Optional['models.AppBskyEmbedDefs.AspectRatio'] = None,
    ) -> 'models.AppBskyFeedPost.CreateRecordResponse':
        """Send post with attached image.

        Note:
            If `profile_identify` is not provided will be sent to the current profile.

        Args:
            text: Text of the post.
            image: Binary image to attach.
            image_alt: Text version of the image.
            profile_identify: Handle or DID. Where to send post.
            reply_to: Root and parent of the post to reply to.
            langs: List of used languages in the post.
            facets: List of facets (rich text items).
            image_aspect_ratio: Aspect ratio of the image.

        Returns:
            :obj:`models.AppBskyFeedPost.CreateRecordResponse`: Reference to the created record.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        image_aspect_ratios = None
        if image_aspect_ratio:
            image_aspect_ratios = [image_aspect_ratio]

        return self.send_images(
            text,
            images=[image],
            image_alts=[image_alt],
            profile_identify=profile_identify,
            reply_to=reply_to,
            langs=langs,
            facets=facets,
            image_aspect_ratios=image_aspect_ratios,
        )

    def send_video(
        self,
        text: t.Union[str, TextBuilder],
        video: bytes,
        video_alt: t.Optional[str] = None,
        profile_identify: t.Optional[str] = None,
        reply_to: t.Optional['models.AppBskyFeedPost.ReplyRef'] = None,
        langs: t.Optional[t.List[str]] = None,
        facets: t.Optional[t.List['models.AppBskyRichtextFacet.Main']] = None,
        video_aspect_ratio: t.Optional['models.AppBskyEmbedDefs.AspectRatio'] = None,
    ) -> 'models.AppBskyFeedPost.CreateRecordResponse':
        """Send post with attached video.

        Note:
            If `profile_identify` is not provided will be sent to the current profile.

        Args:
            text: Text of the post.
            video: Binary video to attach.
            video_alt: Text version of the video.
            profile_identify: Handle or DID. Where to send post.
            reply_to: Root and parent of the post to reply to.
            langs: List of used languages in the post.
            facets: List of facets (rich text items).
            video_aspect_ratio: Aspect ratio of the video.

        Returns:
            :obj:`models.AppBskyFeedPost.CreateRecordResponse`: Reference to the created record.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        if video_alt is None:
            video_alt = ''

        upload = self.upload_blob(video)

        return self.send_post(
            text,
            profile_identify=profile_identify,
            reply_to=reply_to,
            embed=models.AppBskyEmbedVideo.Main(video=upload.blob, alt=video_alt, aspect_ratio=video_aspect_ratio),
            langs=langs,
            facets=facets,
        )

    def get_post(
        self, post_rkey: str, profile_identify: t.Optional[str] = None, cid: t.Optional[str] = None
    ) -> 'models.AppBskyFeedPost.GetRecordResponse':
        """Get post.

        Args:
            post_rkey: ID (slug) of the post.
            profile_identify: Handler or DID. Who created the post.
            cid: The CID of the version of the post.

        Returns:
            :obj:`models.AppBskyFeedPost.GetRecordResponse`: Post.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        repo = self.me and self.me.did
        if profile_identify:
            repo = profile_identify

        if not repo:
            raise LoginRequiredError

        return self.app.bsky.feed.post.get(repo, post_rkey, cid)

    def get_posts(self, uris: t.List[str]) -> 'models.AppBskyFeedGetPosts.Response':
        """Get posts.

        Args:
            uris: Uris (AT URI).

        Example:
            .. code-block:: python

                client.get_posts(['at://did:plc:kvwvcn5iqfooopmyzvb4qzba/app.bsky.feed.post/3k2yihcrp6f2c'])

        Returns:
            :obj:`models.AppBskyFeedGetPosts.Response`: Posts.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.feed.get_posts(
            models.AppBskyFeedGetPosts.Params(
                uris=uris,
            )
        )

    def get_post_thread(
        self, uri: str, depth: t.Optional[int] = None, parent_height: t.Optional[int] = None
    ) -> 'models.AppBskyFeedGetPostThread.Response':
        """Get post thread.

        Args:
            uri: AT URI.
            depth: Depth of the thread.
            parent_height: Height of the parent post.

        Returns:
            :obj:`models.AppBskyFeedGetPostThread.Response`: Post thread.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.feed.get_post_thread(
            models.AppBskyFeedGetPostThread.Params(
                uri=uri,
                depth=depth,
                parent_height=parent_height,
            )
        )

    def get_likes(
        self, uri: str, cid: t.Optional[str] = None, cursor: t.Optional[str] = None, limit: t.Optional[int] = None
    ) -> 'models.AppBskyFeedGetLikes.Response':
        """Get likes.

        Args:
            uri: AT URI.
            cid: CID.
            cursor: Cursor of the last like in the previous page.
            limit: Limit count of likes to return.

        Returns:
            :obj:`models.AppBskyFeedGetLikes.Response`: Likes.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.feed.get_likes(
            models.AppBskyFeedGetLikes.Params(uri=uri, cid=cid, cursor=cursor, limit=limit)
        )

    def get_reposted_by(
        self, uri: str, cid: t.Optional[str] = None, cursor: t.Optional[str] = None, limit: t.Optional[int] = None
    ) -> 'models.AppBskyFeedGetRepostedBy.Response':
        """Get reposted by (reposts).

        Args:
            uri: AT URI.
            cid: CID.
            cursor: Cursor of the last like in the previous page.
            limit: Limit count of likes to return.

        Returns:
            :obj:`models.AppBskyFeedGetRepostedBy.Response`: Reposts.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.feed.get_reposted_by(
            models.AppBskyFeedGetRepostedBy.Params(uri=uri, cid=cid, cursor=cursor, limit=limit)
        )

    def get_timeline(
        self, algorithm: t.Optional[str] = None, cursor: t.Optional[str] = None, limit: t.Optional[int] = None
    ) -> 'models.AppBskyFeedGetTimeline.Response':
        """Get home timeline.

        Args:
            algorithm: Algorithm.
            cursor: Cursor of the last like in the previous page.
            limit: Limit count of likes to return.

        Returns:
            :obj:`models.AppBskyFeedGetTimeline.Response`: Home timeline.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.feed.get_timeline(
            models.AppBskyFeedGetTimeline.Params(algorithm=algorithm, cursor=cursor, limit=limit)
        )

    def get_author_feed(
        self,
        actor: str,
        cursor: t.Optional[str] = None,
        filter: t.Optional[str] = None,
        limit: t.Optional[int] = None,
        include_pins: bool = False,
    ) -> 'models.AppBskyFeedGetAuthorFeed.Response':
        """Get author (profile) feed.

        Args:
            actor: Actor (handle or DID).
            cursor: Cursor of the last like in the previous page.
            filter: Filter.
            limit: Limit count of likes to return.
            include_pins: Include pins.

        Returns:
            :obj:`models.AppBskyFeedGetAuthorFeed.Response`: Feed.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.feed.get_author_feed(
            models.AppBskyFeedGetAuthorFeed.Params(
                actor=actor, cursor=cursor, filter=filter, include_pins=include_pins, limit=limit
            )
        )

    def like(self, uri: str, cid: str) -> 'models.AppBskyFeedLike.CreateRecordResponse':
        """Like the record.

        Args:
            cid: The CID of the record.
            uri: The URI of the record.

        Note:
            Record could be post, custom feed, etc.

        Returns:
            :obj:`models.AppBskyFeedLike.CreateRecordResponse`: Reference to the created record.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        subject_obj = models.ComAtprotoRepoStrongRef.Main(cid=cid, uri=uri)

        repo = self.me and self.me.did
        if not repo:
            raise LoginRequiredError

        record = models.AppBskyFeedLike.Record(created_at=self.get_current_time_iso(), subject=subject_obj)
        return self.app.bsky.feed.like.create(repo, record)

    def unlike(self, like_uri: str) -> bool:
        """Unlike the post.

        Args:
            like_uri: AT URI of the like.

        Returns:
            :obj:`bool`: Success status.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        uri = AtUri.from_str(like_uri)
        return self.app.bsky.feed.like.delete(uri.hostname, uri.rkey)

    def repost(self, uri: str, cid: str) -> 'models.AppBskyFeedRepost.CreateRecordResponse':
        """Repost post.

        Args:
            cid: The CID of the post.
            uri: The URI of the post.

        Returns:
            :obj:`models.AppBskyFeedRepost.CreateRecordResponse`: Reference to the reposted record.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        subject_obj = models.ComAtprotoRepoStrongRef.Main(cid=cid, uri=uri)

        repo = self.me and self.me.did
        if not repo:
            raise LoginRequiredError

        record = models.AppBskyFeedRepost.Record(created_at=self.get_current_time_iso(), subject=subject_obj)
        return self.app.bsky.feed.repost.create(repo, record)

    def unrepost(self, repost_uri: str) -> bool:
        """Unrepost the post (delete repost).

        Args:
            repost_uri: AT URI of the repost.

        Returns:
            :obj:`bool`: Success status.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        uri = AtUri.from_str(repost_uri)
        return self.app.bsky.feed.repost.delete(uri.hostname, uri.rkey)

    def follow(self, subject: str) -> 'models.AppBskyGraphFollow.CreateRecordResponse':
        """Follow the profile.

        Args:
            subject: DID of the profile.

        Returns:
            :obj:`models.AppBskyGraphFollow.CreateRecordResponse`: Reference to the created record.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        repo = self.me and self.me.did
        if not repo:
            raise LoginRequiredError

        record = models.AppBskyGraphFollow.Record(created_at=self.get_current_time_iso(), subject=subject)
        return self.app.bsky.graph.follow.create(repo, record)

    def unfollow(self, follow_uri: str) -> bool:
        """Unfollow the profile.

        Args:
            follow_uri: AT URI of the follow.

        Returns:
            :obj:`bool`: Success status.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        uri = AtUri.from_str(follow_uri)
        return self.app.bsky.graph.follow.delete(uri.hostname, uri.rkey)

    def get_follows(
        self, actor: str, cursor: t.Optional[str] = None, limit: t.Optional[int] = None
    ) -> 'models.AppBskyGraphGetFollows.Response':
        """Get follows of the profile.

        Args:
            actor: Actor (handle or DID).
            cursor: Cursor of the next page.
            limit: Limit count of follows to return.

        Returns:
            :obj:`models.AppBskyGraphGetFollows.Response`: Follows.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.graph.get_follows(
            models.AppBskyGraphGetFollows.Params(actor=actor, cursor=cursor, limit=limit)
        )

    def get_followers(
        self, actor: str, cursor: t.Optional[str] = None, limit: t.Optional[int] = None
    ) -> 'models.AppBskyGraphGetFollowers.Response':
        """Get followers of the profile.

        Args:
            actor: Actor (handle or DID).
            cursor: Cursor of the next page.
            limit: Limit count of followers to return.

        Returns:
            :obj:`models.AppBskyGraphGetFollowers.Response`: Followers.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.graph.get_followers(
            models.AppBskyGraphGetFollowers.Params(actor=actor, cursor=cursor, limit=limit)
        )

    def get_profile(self, actor: str) -> 'models.AppBskyActorDefs.ProfileViewDetailed':
        """Get profile.

        Args:
            actor: Actor (handle or DID).

        Returns:
            :obj:`models.AppBskyActorDefs.ProfileViewDetailed`: Profile.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.actor.get_profile(models.AppBskyActorGetProfile.Params(actor=actor))

    def get_profiles(self, actors: t.List[str]) -> 'models.AppBskyActorGetProfiles.Response':
        """Get profiles.

        Args:
            actors: List of actors (handles or DIDs).

        Returns:
            :obj:`models.AppBskyActorGetProfiles.Response`: Profiles.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.actor.get_profiles(models.AppBskyActorGetProfiles.Params(actors=actors))

    def mute(self, actor: str) -> bool:
        """Mute actor (profile).

        Args:
            actor: Actor (handle or DID).

        Returns:
            :obj:`bool`: Success status.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.graph.mute_actor(models.AppBskyGraphMuteActor.Data(actor=actor))

    def unmute(self, actor: str) -> bool:
        """Unmute actor (profile).

        Args:
            actor: Actor (handle or DID).

        Returns:
            :obj:`bool`: Success status.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.app.bsky.graph.unmute_actor(models.AppBskyGraphUnmuteActor.Data(actor=actor))

    def resolve_handle(self, handle: str) -> 'models.ComAtprotoIdentityResolveHandle.Response':
        """Resolve the handle.

        Args:
            handle: Handle.

        Returns:
            :obj:`models.ComAtprotoIdentityResolveHandle.Response`: Resolved handle (DID).

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.com.atproto.identity.resolve_handle(models.ComAtprotoIdentityResolveHandle.Params(handle=handle))

    def update_handle(self, handle: str) -> bool:
        """Update the handle.

        Args:
            handle: New handle.

        Returns:
            :obj:`bool`: Success status.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.com.atproto.identity.update_handle(models.ComAtprotoIdentityUpdateHandle.Data(handle=handle))

    def upload_blob(self, data: bytes) -> 'models.ComAtprotoRepoUploadBlob.Response':
        """Upload blob.

        Args:
            data: Binary data.

        Returns:
            :obj:`models.ComAtprotoRepoUploadBlob.Response`: Uploaded blob reference.

        Raises:
            :class:`atproto.exceptions.AtProtocolError`: Base exception.
        """
        return self.com.atproto.repo.upload_blob(data)

    #: Alias for :attr:`unfollow`
    delete_follow = unfollow
    #: Alias for :attr:`unlike`
    delete_like = unlike
    #: Alias for :attr:`unrepost`
    delete_repost = unrepost
    #: Alias for :attr:`send_post`
    post = send_post
    #: Alias for :attr:`delete_post`
    unsend = delete_post
