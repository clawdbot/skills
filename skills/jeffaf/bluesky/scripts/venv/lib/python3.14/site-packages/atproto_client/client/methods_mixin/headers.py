import typing as t
from enum import Enum

import typing_extensions as te
from atproto_core.exceptions import AtProtocolError

_ATPROTO_PROXY_HEADER = 'atproto-proxy'
_ATPROTO_ACCEPT_LABELERS_HEADER = 'atproto-accept-labelers'


class HeadersConfigurationMethodsMixin:
    BSKY_CHAT_DID: t.ClassVar[t.Literal['did:web:api.bsky.chat']] = 'did:web:api.bsky.chat'

    # Bluesky hardcoded labeler https://docs.bsky.app/blog/blueskys-moderation-architecture
    BSKY_LABELER_DID: t.ClassVar[t.Literal['did:plc:ar7c4by46qjdydhdevvrndac']] = 'did:plc:ar7c4by46qjdydhdevvrndac'

    class AtprotoServiceType(Enum):
        """The type of atproto service."""

        ATPROTO_LABELER = 'atproto_labeler'
        BSKY_CHAT = 'bsky_chat'

    def clone(self) -> te.Self:
        """Clone the client instance.

        Used to customize atproto proxy and set of labeler services.

        Returns:
            Cloned client instance.
        """
        cloned_client = super().clone()

        # share the same objects to avoid conflicts with session changes
        cloned_client.me = self.me
        cloned_client._session = self._session
        cloned_client._session_dispatcher = self._session_dispatcher

        return cloned_client

    def with_proxy(self, service_type: t.Union[AtprotoServiceType, str], did: str) -> te.Self:
        """Get a new client instance with the atproto-proxy header configured.

        Args:
            service_type: The type of service.
            did: The DID of the proxy.

        Returns:
            :obj:`self`: Configured client instance.
        """
        cloned_client = self.clone()
        cloned_client.configure_proxy_header(service_type, did)
        return cloned_client

    def with_labelers(self, labeler_dids: t.List[str]) -> te.Self:
        """Get a new client instance with the atproto-accept-labelers header configured.

        Args:
            labeler_dids: The DIDs of the labelers.

        Returns:
            :obj:`self`: Configured client instance.
        """
        cloned_client = self.clone()
        cloned_client.configure_labelers_header(labeler_dids)
        return cloned_client

    def configure_proxy_header(self, service_type: t.Union[AtprotoServiceType, str], did: str) -> None:
        """Configure the atproto-proxy header to be applied on requests.

        Args:
            service_type: The type of service.
            did: The DID of the proxy.
        """
        if not did.startswith('did:'):
            raise AtProtocolError('Invalid DID format')

        if isinstance(service_type, self.AtprotoServiceType):
            service_type = service_type.value

        proxy_header = f'{did}#{service_type}'
        self.request.add_additional_header(_ATPROTO_PROXY_HEADER, proxy_header)

    def configure_labelers_header(self, labeler_dids: t.List[str]) -> None:
        """Configure the atproto-labelers header to be applied on requests.

        Args:
            labeler_dids: The DIDs of the labelers.
        """
        labelers_prepared = [f'{labeler_did};redact' for labeler_did in labeler_dids if labeler_did.startswith('did:')]
        labelers_header_value = ','.join(labelers_prepared)

        self.request.add_additional_header(_ATPROTO_ACCEPT_LABELERS_HEADER, labelers_header_value)

    def with_bsky_chat_proxy(self) -> te.Self:
        """Get a new client instance with the atproto-proxy header configured for bsky.chat.

        Returns:
            :obj:`self`: Configured client instance.
        """
        return self.with_proxy(self.AtprotoServiceType.BSKY_CHAT, self.BSKY_CHAT_DID)

    def with_bsky_labeler(self) -> te.Self:
        """Get a new client instance with the atproto-accept-labelers header configured for Bluesky Labeler.

        Returns:
            :obj:`self`: Configured client instance.
        """
        return self.with_labelers([self.BSKY_LABELER_DID])
