import typing as t

import httpx
from pydantic_core import from_json

from atproto_identity.did.resolvers.base_resolver import AsyncBaseResolver, BaseResolver
from atproto_identity.exceptions import DidWebResolverError, PoorlyFormattedDidError, UnsupportedDidWebPathError

if t.TYPE_CHECKING:
    from atproto_identity.cache.base_cache import AsyncDidBaseCache, DidBaseCache

_DID_DOC_PATH = '/.well-known/did.json'


class _DidWebResolverBase:
    @staticmethod
    def _parse_web_did(did: str) -> str:
        parsed_id = ':'.join(did.split(':')[2:])
        parts = parsed_id.split(':')

        if not parts:
            raise PoorlyFormattedDidError(f'Invalid DID {did}')

        if len(parts) > 1:
            raise UnsupportedDidWebPathError(f'Unsupported DID {did}')

        path = parts[0] + _DID_DOC_PATH
        return f'https://{path}'


class DidWebResolver(_DidWebResolverBase, BaseResolver):
    def __init__(
        self,
        timeout: t.Optional[float] = None,
        cache: t.Optional['DidBaseCache'] = None,
    ) -> None:
        super().__init__(cache)

        self._timeout = timeout

        self._client = httpx.Client()

    def resolve_without_validation(self, did: str) -> t.Dict[str, t.Any]:
        url = self._parse_web_did(did)

        try:
            response = self._client.get(url, timeout=self._timeout)
            response.raise_for_status()
            return from_json(response.content)
        except httpx.HTTPError as e:
            raise DidWebResolverError(f'Error resolving DID {did}') from e


class AsyncDidWebResolver(_DidWebResolverBase, AsyncBaseResolver):
    def __init__(
        self,
        timeout: t.Optional[float] = None,
        cache: t.Optional['AsyncDidBaseCache'] = None,
    ) -> None:
        super().__init__(cache)

        self._timeout = timeout

        self._client = httpx.AsyncClient()

    async def resolve_without_validation(self, did: str) -> t.Dict[str, t.Any]:
        url = self._parse_web_did(did)

        try:
            response = await self._client.get(url, timeout=self._timeout)
            response.raise_for_status()
            return from_json(response.content)
        except httpx.HTTPError as e:
            raise DidWebResolverError(f'Error resolving DID {did}') from e
