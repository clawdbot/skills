import typing as t

import httpx
from pydantic_core import from_json

from atproto_identity.did.resolvers.base_resolver import AsyncBaseResolver, BaseResolver
from atproto_identity.exceptions import DidPlcResolverError

if t.TYPE_CHECKING:
    from atproto_identity.cache.base_cache import AsyncDidBaseCache, DidBaseCache


class DidPlcResolver(BaseResolver):
    def __init__(
        self,
        plc_url: t.Optional[str] = None,
        timeout: t.Optional[float] = None,
        cache: t.Optional['DidBaseCache'] = None,
    ) -> None:
        super().__init__(cache)

        self._plc_url = plc_url
        self._timeout = timeout

        self._client = httpx.Client()

    def resolve_without_validation(self, did: str) -> t.Optional[t.Dict[str, t.Any]]:
        try:
            response = self._client.get(f'{self._plc_url}/{did}', timeout=self._timeout)

            if response.status_code == 404:
                return None

            response.raise_for_status()
            return from_json(response.content)
        except httpx.HTTPError as e:
            raise DidPlcResolverError(f'Error resolving DID {did}') from e


class AsyncDidPlcResolver(AsyncBaseResolver):
    def __init__(
        self,
        plc_url: t.Optional[str] = None,
        timeout: t.Optional[float] = None,
        cache: t.Optional['AsyncDidBaseCache'] = None,
    ) -> None:
        super().__init__(cache)

        self._plc_url = plc_url
        self._timeout = timeout

        self._client = httpx.AsyncClient()

    async def resolve_without_validation(self, did: str) -> t.Optional[t.Dict[str, t.Any]]:
        try:
            response = await self._client.get(f'{self._plc_url}/{did}', timeout=self._timeout)

            if response.status_code == 404:
                return None

            response.raise_for_status()
            return from_json(response.content)
        except httpx.HTTPError as e:
            raise DidPlcResolverError(f'Error resolving DID {did}') from e
