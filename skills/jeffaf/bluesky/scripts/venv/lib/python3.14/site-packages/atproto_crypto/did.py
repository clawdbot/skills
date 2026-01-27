import typing as t
from dataclasses import dataclass

from atproto_crypto.algs.p256 import P256
from atproto_crypto.algs.secp256k1 import Secp256k1
from atproto_crypto.consts import (
    BASE58_MULTIBASE_PREFIX,
    DID_KEY_PREFIX,
    P256_DID_PREFIX,
    P256_JWT_ALG,
    SECP256K1_DID_PREFIX,
    SECP256K1_JWT_ALG,
)
from atproto_crypto.exceptions import IncorrectDidKeyPrefixError, IncorrectMultikeyPrefixError, UnsupportedKeyTypeError
from atproto_crypto.multibase import bytes_to_multibase, multibase_to_bytes


@dataclass
class Multikey:
    jwt_alg: str
    key_bytes: bytes

    @staticmethod
    def from_str(multikey: str) -> 'Multikey':
        """Create multikey from string.

        Args:
            multikey: Multikey.

        Returns:
            :obj:`Multikey`: Multikey.
        """
        return parse_multikey(multikey)

    def to_str(self) -> str:
        """Format multikey.

        Returns:
            str: Multikey.
        """
        return format_multikey(self.jwt_alg, self.key_bytes)


def get_multikey_alg(multikey: str) -> str:
    """Get JWT alg for multikey.

    Args:
        multikey: Multikey.

    Returns:
        str: JWT alg.
    """
    if not multikey.startswith(BASE58_MULTIBASE_PREFIX):
        raise IncorrectMultikeyPrefixError(f'Incorrect prefix for multikey {multikey}')

    prefixed_bytes = multibase_to_bytes(multikey)
    if prefixed_bytes.startswith(P256_DID_PREFIX):
        return P256_JWT_ALG
    if prefixed_bytes.startswith(SECP256K1_DID_PREFIX):
        return SECP256K1_JWT_ALG

    raise UnsupportedKeyTypeError('Unsupported key type')


def parse_multikey(multikey: str) -> Multikey:
    """Parse multikey.

    Args:
        multikey: Multikey.

    Returns:
        :obj:`Multikey`: Multikey.

    Raises:
        :obj:`IncorrectMultikeyPrefixError`: Incorrect prefix for multikey.
        :obj:`UnsupportedKeyTypeError`: Unsupported key type.
    """
    if not multikey.startswith(BASE58_MULTIBASE_PREFIX):
        raise IncorrectMultikeyPrefixError(f'Incorrect prefix for multikey {multikey}')

    prefixed_bytes = multibase_to_bytes(multikey)
    if prefixed_bytes.startswith(P256_DID_PREFIX):
        jwt_alg = P256_JWT_ALG
        compressed_key_bytes = prefixed_bytes[len(P256_DID_PREFIX) :]
        key_bytes = P256().decompress_pubkey(compressed_key_bytes)
    elif prefixed_bytes.startswith(SECP256K1_DID_PREFIX):
        jwt_alg = SECP256K1_JWT_ALG
        compressed_key_bytes = prefixed_bytes[len(SECP256K1_DID_PREFIX) :]
        key_bytes = Secp256k1().decompress_pubkey(compressed_key_bytes)
    else:
        raise UnsupportedKeyTypeError('Unsupported key type')

    return Multikey(jwt_alg, key_bytes)


def format_multikey(jwt_alg: str, key: bytes) -> str:
    """Format multikey to multibase.

    Compress pubkey and encode with base58btc.

    Args:
        jwt_alg: JWT alg.
        key: Key bytes.

    Returns:
        str: Multikey in multibase.

    Raises:
        :obj:`UnsupportedKeyTypeError`: Unsupported key type.
    """
    if jwt_alg == P256_JWT_ALG:
        prefix = P256_DID_PREFIX
        compressed_key_bytes = P256().compress_pubkey(key)
    elif jwt_alg == SECP256K1_JWT_ALG:
        prefix = SECP256K1_DID_PREFIX
        compressed_key_bytes = Secp256k1().compress_pubkey(key)
    else:
        raise UnsupportedKeyTypeError('Unsupported key type')

    prefixed_bytes = prefix + compressed_key_bytes
    return bytes_to_multibase(BASE58_MULTIBASE_PREFIX, prefixed_bytes)


def parse_did_key(did_key: str) -> Multikey:
    """Parse DID key.

    Args:
        did_key: DID key.

    Returns:
        :obj:`Multikey`: Multikey.

    Raises:
        :obj:`IncorrectDidKeyPrefixError`: Incorrect prefix for DID key.
    """
    if not did_key.startswith(DID_KEY_PREFIX):
        raise IncorrectDidKeyPrefixError(f'Incorrect prefix for DID key {did_key}')

    return parse_multikey(did_key[len(DID_KEY_PREFIX) :])


def format_did_key(jwt_alg: str, key: bytes) -> str:
    """Format DID key.

    Args:
        jwt_alg: JWT alg.
        key: Key bytes.

    Returns:
        str: DID key.
    """
    return f'{DID_KEY_PREFIX}{format_multikey(jwt_alg, key)}'


def format_did_key_multikey(multikey: str) -> str:
    """Format DID key from multikey.

    Args:
        multikey: Multikey.

    Returns:
        :obj:`str`: DID key.
    """
    return f'{DID_KEY_PREFIX}{multikey}'


def get_did_key(key_type: str, key: str) -> t.Optional[str]:
    """Get DID key.

    Args:
        key_type: Key type.
        key: Key.

    Returns:
        :obj:`str`: DID key or ``None`` if a key type is not supported.
    """
    did_key = None
    if key_type == 'EcdsaSecp256r1VerificationKey2019':
        key_bytes = multibase_to_bytes(key)
        did_key = format_did_key(P256_JWT_ALG, key_bytes)
    elif key_type == 'EcdsaSecp256k1VerificationKey2019':
        key_bytes = multibase_to_bytes(key)
        did_key = format_did_key(SECP256K1_JWT_ALG, key_bytes)
    elif key_type == 'Multikey':
        # Multikey is compressed already
        did_key = format_did_key_multikey(key)

    return did_key
