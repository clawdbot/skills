import typing as t

if t.TYPE_CHECKING:
    from atproto_client.client.async_raw import AsyncClientRaw
    from atproto_client.client.raw import ClientRaw


class NamespaceBase:
    def __init__(self, client: 'ClientRaw') -> None:
        self._client: 'ClientRaw' = client


class AsyncNamespaceBase:
    def __init__(self, client: 'AsyncClientRaw') -> None:
        self._client: 'AsyncClientRaw' = client


class RecordBase:
    def __init__(self, client: 'ClientRaw') -> None:
        self._client: 'ClientRaw' = client


class AsyncRecordBase:
    def __init__(self, client: 'AsyncClientRaw') -> None:
        self._client: 'AsyncClientRaw' = client
