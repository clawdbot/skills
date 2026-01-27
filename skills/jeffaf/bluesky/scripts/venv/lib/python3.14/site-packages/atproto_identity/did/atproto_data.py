import typing as t
from dataclasses import dataclass

from atproto_identity.exceptions import AtprotoDataParseError

if t.TYPE_CHECKING:
    from atproto_core.did_doc import DidDocument


@dataclass
class AtprotoData:
    """Dataclass for atproto data."""

    did: str
    signing_key: t.Optional[str] = None
    handle: t.Optional[str] = None
    pds: t.Optional[str] = None

    @classmethod
    def from_did_doc(cls, did_doc: 'DidDocument') -> 'AtprotoData':
        """Create AT Protocol data from DID document.

        Args:
            did_doc: DID document.

        Returns:
            :obj:`AtprotoData`: AT Protocol data.
        """
        return AtprotoData(
            did=did_doc.id,
            signing_key=did_doc.get_did_key(),
            handle=did_doc.get_handle(),
            pds=did_doc.get_pds_endpoint(),
        )


def ensure_atproto_document(did_doc: 'DidDocument') -> AtprotoData:
    """Ensure that the DID document is an AT Protocol DID document.

    Args:
        did_doc: DID document.

    Returns:
        :obj:`AtprotoData`: AT Protocol data.

    Raises:
        :obj:`AtprotoDataParseError`: If the DID document is not an AT Protocol DID document.
    """
    atproto_data = AtprotoData.from_did_doc(did_doc)

    if atproto_data.signing_key is None:
        raise AtprotoDataParseError(f'Could not parse signing_key from doc: {did_doc}')
    if atproto_data.handle is None:
        raise AtprotoDataParseError(f'Could not parse handle from doc: {did_doc}')
    if atproto_data.pds is None:
        raise AtprotoDataParseError(f'Could not parse pds from doc: {did_doc}')

    return atproto_data


def ensure_atproto_key(did_doc: 'DidDocument') -> str:
    """Ensure that the DID document has AT Protocol signing key.

    Args:
        did_doc: DID document.

    Returns:
        :obj:`str`: AT Protocol signing key.

    Raises:
        :obj:`AtprotoDataParseError`: If the DID document does not have an AT Protocol signing key.
    """
    atproto_data = AtprotoData.from_did_doc(did_doc)

    if atproto_data.signing_key is None:
        raise AtprotoDataParseError(f'Could not parse signing_key from doc: {did_doc}')

    return atproto_data.signing_key
