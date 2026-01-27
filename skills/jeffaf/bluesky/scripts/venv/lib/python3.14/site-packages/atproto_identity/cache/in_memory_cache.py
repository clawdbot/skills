import typing as t
from datetime import datetime, timezone

from atproto_core.did_doc import DidDocument

from atproto_identity.cache.base_cache import AsyncDidBaseCache, DidBaseCache
from atproto_identity.cache.models import CachedDid, CachedDidResult

if t.TYPE_CHECKING:
    from atproto_identity.cache.base_cache import AsyncGetDocCallback, GetDocCallback


def _datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class DidInMemoryCache(DidBaseCache):
    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)

        self._cache: t.Dict[str, CachedDid] = {}

    def set(self, did: str, document: DidDocument) -> None:
        self._cache[did] = CachedDid(document, _datetime_now())

    def refresh(self, did: str, get_doc_callback: 'GetDocCallback') -> None:
        doc = get_doc_callback()
        if doc:
            self.set(did, doc)

    def delete(self, did: str) -> None:
        del self._cache[did]

    def clear(self) -> None:
        self._cache.clear()

    def get(self, did: str) -> t.Optional[CachedDidResult]:
        val = self._cache.get(did)
        if not val:
            return None

        now = _datetime_now().timestamp()
        expired = now > val.updated_at.timestamp() + self.max_ttl
        stale = now > val.updated_at.timestamp() + self.stale_ttl

        return CachedDidResult(did, val.document, val.updated_at, stale, expired)


class AsyncDidInMemoryCache(AsyncDidBaseCache):
    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)

        self._in_memory_cache = DidInMemoryCache(*args, **kwargs)

    async def set(self, did: str, document: DidDocument) -> None:
        self._in_memory_cache.set(did, document)

    async def refresh(self, did: str, get_doc_callback: 'AsyncGetDocCallback') -> None:
        doc = await get_doc_callback()
        if doc:
            await self.set(did, doc)

    async def delete(self, did: str) -> None:
        self._in_memory_cache.delete(did)

    async def clear(self) -> None:
        self._in_memory_cache.clear()

    async def get(self, did: str) -> t.Optional[CachedDidResult]:
        return self._in_memory_cache.get(did)
