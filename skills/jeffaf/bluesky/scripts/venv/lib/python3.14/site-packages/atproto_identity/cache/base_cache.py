import typing as t
from abc import ABC, abstractmethod

if t.TYPE_CHECKING:
    from atproto_core.did_doc import DidDocument

    from atproto_identity.cache.models import CachedDidResult


_DEFAULT_STALE_TTL = 60 * 60  # 1 hour
_DEFAULT_MAX_TTL = 60 * 60 * 24  # 1 day


GetDocCallback = t.Callable[[], t.Optional['DidDocument']]
AsyncGetDocCallback = t.Callable[[], t.Coroutine[t.Any, t.Any, t.Optional['DidDocument']]]


class _DidBaseCache:
    def __init__(self, stale_ttl: t.Optional[int] = None, max_ttl: t.Optional[int] = None) -> None:
        self.stale_ttl = stale_ttl or _DEFAULT_STALE_TTL
        self.max_ttl = max_ttl or _DEFAULT_MAX_TTL


class DidBaseCache(_DidBaseCache, ABC):
    """Abstract DID Cache.

    Args:
        stale_ttl: Stale TTL in seconds. Default is 1 hour.
        max_ttl: Max TTL in seconds. Default is 1 day.
    """

    def __init__(self, stale_ttl: t.Optional[int] = None, max_ttl: t.Optional[int] = None) -> None:
        super().__init__(stale_ttl, max_ttl)

    @abstractmethod
    def get(self, did: str) -> t.Optional['CachedDidResult']:
        """Get cached DID.

        Args:
            did: DID.

        Returns:
            :obj:`CachedDidResult`: Cached DID result or ``None`` if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def set(self, did: str, document: 'DidDocument') -> None:
        """Set cached DID.

        Args:
            did: DID.
            document: DID document.
        """
        raise NotImplementedError

    @abstractmethod
    def refresh(self, did: str, get_doc_callback: GetDocCallback) -> None:
        """Refresh cached DID.

        Args:
            did: DID.
            get_doc_callback: Get DID document callback.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, did: str) -> None:
        """Delete cached DID.

        Args:
            did: DID.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """Clear cached DIDs.

        Note:
            This method is used to clear all cached DIDs.
        """
        raise NotImplementedError


class AsyncDidBaseCache(_DidBaseCache, ABC):
    """Asynchronous Abstract DID Cache.

    Args:
        stale_ttl: Stale TTL in seconds. Default is 1 hour.
        max_ttl: Max TTL in seconds. Default is 1 day.
    """

    def __init__(self, stale_ttl: t.Optional[int] = None, max_ttl: t.Optional[int] = None) -> None:
        super().__init__(stale_ttl, max_ttl)

    @abstractmethod
    async def get(self, did: str) -> t.Optional['CachedDidResult']:
        """Get cached DID.

        Args:
            did: DID.

        Returns:
            :obj:`CachedDidResult`: Cached DID result or ``None`` if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def set(self, did: str, document: 'DidDocument') -> None:
        """Set cached DID.

        Args:
            did: DID.
            document: DID document.
        """
        raise NotImplementedError

    @abstractmethod
    async def refresh(self, did: str, get_doc_callback: AsyncGetDocCallback) -> None:
        """Refresh cached DID.

        Args:
            did: DID.
            get_doc_callback: Get DID document callback.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, did: str) -> None:
        """Delete cached DID.

        Args:
            did: DID.
        """
        raise NotImplementedError

    @abstractmethod
    async def clear(self) -> None:
        """Clear cached DIDs.

        Note:
            This method is used to clear all cached DIDs.
        """
        raise NotImplementedError
