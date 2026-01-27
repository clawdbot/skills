import typing as t

from atproto_identity.did.resolvers.base_resolver import AsyncBaseResolver, BaseResolver
from atproto_identity.did.resolvers.plc_resolver import AsyncDidPlcResolver, DidPlcResolver
from atproto_identity.did.resolvers.web_resolver import AsyncDidWebResolver, DidWebResolver
from atproto_identity.exceptions import PoorlyFormattedDidError, UnsupportedDidMethodError

if t.TYPE_CHECKING:
    from atproto_identity.cache.base_cache import AsyncDidBaseCache, DidBaseCache


_BASE_PLC_URL = 'https://plc.directory'
_DEFAULT_TIMEOUT = 3.0
_DID_PREFIX = 'did'


class _DidResolverBase:
    def __init__(self) -> None:
        self._methods: t.Dict[str, t.Union[BaseResolver, AsyncBaseResolver]] = {}

    def _get_resolver_method(self, did: str) -> t.Union[BaseResolver, AsyncBaseResolver]:
        parts = did.split(':')
        if not parts:
            raise PoorlyFormattedDidError(f'Invalid DID {did}')

        if parts[0] != _DID_PREFIX:
            raise PoorlyFormattedDidError(f'Invalid DID {did}')

        if len(parts) < 2:
            raise PoorlyFormattedDidError(f'Invalid DID {did}')

        method = parts[1]
        if method not in self._methods:
            raise UnsupportedDidMethodError(f'Invalid DID {did}')

        return self._methods[method]


class DidResolver(_DidResolverBase, BaseResolver):
    """DID Resolver.

    Supported DID methods: PLC, Web.

    Args:
        plc_url: PLC directory URL.
        timeout: Request timeout.
        cache: DID cache.
    """

    def __init__(
        self,
        plc_url: t.Optional[str] = None,
        timeout: t.Optional[float] = None,
        cache: t.Optional['DidBaseCache'] = None,
    ) -> None:
        super().__init__()
        BaseResolver.__init__(self, cache)

        if plc_url is None:
            plc_url = _BASE_PLC_URL

        if timeout is None:
            timeout = _DEFAULT_TIMEOUT

        self._methods = {'plc': DidPlcResolver(plc_url, timeout, cache), 'web': DidWebResolver(timeout)}

    def resolve_without_validation(self, did: str) -> t.Optional[t.Dict[str, t.Any]]:
        """Resolve DID without validation.

        Args:
            did: DID.

        Returns:
            :obj:`dict`: DID document or ``None`` if DID not found.
        """
        base_resolver = t.cast('BaseResolver', self._get_resolver_method(did))
        return base_resolver.resolve_without_validation(did)


class AsyncDidResolver(_DidResolverBase, AsyncBaseResolver):
    """Asynchronous DID Resolver.

    Supported DID methods: PLC, Web.

    Args:
        plc_url: PLC directory URL.
        timeout: Request timeout.
        cache: DID cache.
    """

    def __init__(
        self,
        plc_url: t.Optional[str] = None,
        timeout: t.Optional[float] = None,
        cache: t.Optional['AsyncDidBaseCache'] = None,
    ) -> None:
        super().__init__()
        AsyncBaseResolver.__init__(self, cache)

        if plc_url is None:
            plc_url = _BASE_PLC_URL

        if timeout is None:
            timeout = _DEFAULT_TIMEOUT

        self._methods = {'plc': AsyncDidPlcResolver(plc_url, timeout, cache), 'web': AsyncDidWebResolver(timeout)}

    async def resolve_without_validation(self, did: str) -> t.Optional[t.Dict[str, t.Any]]:
        """Resolve DID without validation.

        Args:
            did: DID.

        Returns:
            :obj:`dict`: DID document or ``None`` if DID not found.
        """
        async_base_resolver = t.cast('AsyncBaseResolver', self._get_resolver_method(did))
        return await async_base_resolver.resolve_without_validation(did)
