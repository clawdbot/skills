import typing as t
from dataclasses import dataclass
from urllib.parse import urlparse

from atproto_crypto.did import get_did_key
from atproto_identity.did.atproto_data import AtprotoData
from pydantic import BaseModel, Field, ValidationError

_AT_URI_PREFIX = 'at://'
_AT_URI_PREFIX_LEN = len(_AT_URI_PREFIX)
_ATPROTO_KEY_ID = '#atproto'


@dataclass
class SigningKey:
    """Public signing key for the account."""

    type: str
    public_key_multibase: str


def _validate_url(url: str) -> t.Optional[str]:
    try:
        parsed_url = urlparse(url)
    except Exception:  # noqa: BLE001
        return None

    if parsed_url.scheme not in {'http', 'https'}:
        return None
    if parsed_url.hostname is None:
        return None

    return url


def is_valid_did_doc(did_doc: t.Union[t.Dict[str, t.Any], t.Any]) -> bool:
    """Return whether the given DID document is valid.

    Args:
        did_doc: The raw DID document.

    Returns:
        :obj:`bool`: Whether the given DID document is valid.
    """
    try:
        DidDocument.from_dict(did_doc)
        return True
    except ValidationError:
        return False


class VerificationMethod(BaseModel):
    """Verification method."""

    id: str
    type: str
    controller: str
    public_key_multibase: t.Optional[str] = Field(default=None, alias='publicKeyMultibase')


class Service(BaseModel):
    """Service."""

    id: str
    type: str
    service_endpoint: t.Union[str, t.Any] = Field(alias='serviceEndpoint')


class DidDocument(BaseModel):
    """DID document."""

    id: str
    also_known_as: t.Optional[t.List[str]] = Field(default=None, alias='alsoKnownAs')
    verification_method: t.Optional[t.List['VerificationMethod']] = Field(default=None, alias='verificationMethod')
    service: t.Optional[t.List['Service']] = None

    def get_did(self: 'DidDocument') -> str:
        """Return the DID of the given DID document.

        Returns:
            :obj:`str`: The DID of the given DID document.
        """
        return self.id

    def get_handle(self: 'DidDocument') -> t.Optional[str]:
        """Return the handle of the given DID document.

        Returns:
            :obj:`str`: The handle of the given DID document, or ``None`` if not found.
        """
        aka = self.also_known_as
        if not aka:
            return None

        for name in aka:
            if name.startswith(_AT_URI_PREFIX):
                return name[_AT_URI_PREFIX_LEN:]

        return None

    def get_service_endpoint(self: 'DidDocument', id_: str, type_: str) -> t.Optional[str]:
        """Return the service endpoint of the given DID document.

        Args:
            id_: The service ID.
            type_: The service type.

        Returns:
            :obj:`str`: The service endpoint of the given DID document, or ``None`` if not found.
        """
        did = self.get_did()

        services = self.service
        if not services:
            return None

        for service in services:
            if (service.id == id_ or service.id == f'{did}{id_}') and service.type == type_:
                return _validate_url(service.service_endpoint)

        return None

    def get_pds_endpoint(self: 'DidDocument') -> t.Optional[str]:
        """Return the personal data server endpoint of the given DID document.

        Returns:
            :obj:`str`: The personal data server endpoint of the given DID document, or ``None`` if not found.
        """
        return self.get_service_endpoint('#atproto_pds', 'AtprotoPersonalDataServer')

    def get_feed_gen_endpoint(self: 'DidDocument') -> t.Optional[str]:
        """Return the feed generator endpoint of the given DID document.

        Returns:
            :obj:`str`: The feed generator endpoint of the given DID document, or ``None`` if not found.
        """
        return self.get_service_endpoint('#bsky_fg', 'BskyFeedGenerator')

    def get_notif_endpoint(self: 'DidDocument') -> t.Optional[str]:
        """Return the notification endpoint of the given DID document.

        Returns:
            :obj:`str`: The notification endpoint of the given DID document, or ``None`` if not found.
        """
        return self.get_service_endpoint('#bsky_notif', 'BskyNotificationService')

    def get_signing_key(self: 'DidDocument') -> t.Optional['SigningKey']:
        """Return the signing key of the given DID document.

        Returns:
            :obj:`SigningKey`: The signing key of the given DID document, or ``None`` if not found.
        """
        did = self.get_did()

        keys = self.verification_method
        if not keys:
            return None

        for key in keys:
            if (key.id == _ATPROTO_KEY_ID or key.id == f'{did}{_ATPROTO_KEY_ID}') and key.public_key_multibase:
                return SigningKey(type=key.type, public_key_multibase=key.public_key_multibase)

        return None

    def get_did_key(self) -> t.Optional[str]:
        """Return the DID key of the given DID document.

        Returns:
            :obj:`str`: The DID key of the given DID document, or ``None`` if not found.
        """
        key = self.get_signing_key()
        if key is None:
            return None

        return get_did_key(key.type, key.public_key_multibase)

    def to_atproto_data(self) -> AtprotoData:
        """Return the AtprotoData of the given DID document.

        Returns:
            :obj:`AtprotoData`: The AtprotoData of the given DID document.
        """
        return AtprotoData(
            did=self.id,
            signing_key=self.get_did_key(),
            handle=self.get_handle(),
            pds=self.get_pds_endpoint(),
        )

    @classmethod
    def from_dict(cls, did_doc: t.Union[t.Dict[str, t.Any], t.Any]) -> 'DidDocument':
        """Parse a DID document.

        Args:
            did_doc: The raw DID document.

        Returns:
            :obj:`DidDocument`: The parsed DID document.
        """
        if hasattr(did_doc, 'to_dict'):
            return DidDocument(**did_doc.to_dict())

        return DidDocument(**did_doc)
