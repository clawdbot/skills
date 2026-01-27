from atproto_crypto.algs import ALGORITHM_TO_CLASS
from atproto_crypto.did import parse_did_key
from atproto_crypto.exceptions import UnsupportedSignatureAlgorithmError


def verify_signature(did_key: str, signing_input: bytes, signature: bytes) -> bool:
    """Verify signature.

    Args:
        did_key: DID key.
        signing_input: Signing input (data).
        signature: Signature.

    Returns:
        bool: True if signature is valid, False otherwise.
    """
    parsed_did_key = parse_did_key(did_key)
    if parsed_did_key.jwt_alg not in ALGORITHM_TO_CLASS:
        raise UnsupportedSignatureAlgorithmError('Unsupported signature alg')

    algorithm_class = ALGORITHM_TO_CLASS[parsed_did_key.jwt_alg]
    return algorithm_class().verify_signature(parsed_did_key.key_bytes, signing_input, signature)
