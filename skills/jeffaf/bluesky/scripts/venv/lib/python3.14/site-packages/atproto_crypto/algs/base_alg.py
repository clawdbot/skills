from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA, EllipticCurve, EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.hazmat.primitives.hashes import SHA256

from atproto_crypto.exceptions import InvalidCompressedPubkeyError


class AlgBase:
    """Base class for all algorithms."""

    NAME = None

    def __init__(self, curve: EllipticCurve, curve_order: int) -> None:
        self.curve = curve
        self.curve_order = curve_order

    def get_elliptic_curve_public_key(self, pubkey: bytes) -> EllipticCurvePublicKey:
        """Return the elliptic curve public key."""
        return EllipticCurvePublicKey.from_encoded_point(self.curve, pubkey)

    def compress_pubkey(self, pubkey: bytes) -> bytes:
        """Compress a public key."""
        return self.get_elliptic_curve_public_key(pubkey).public_bytes(
            encoding=serialization.Encoding.X962, format=serialization.PublicFormat.CompressedPoint
        )

    def decompress_pubkey(self, pubkey: bytes) -> bytes:
        """Decompress a public key."""
        if len(pubkey) != 33:
            raise InvalidCompressedPubkeyError('Expected 33 byte compress pubkey')

        return self.get_elliptic_curve_public_key(pubkey).public_bytes(
            encoding=serialization.Encoding.X962, format=serialization.PublicFormat.UncompressedPoint
        )

    def _ensure_dss_signature_low_s(self, s: int) -> None:
        """Ensure DSS signature is low-S.

        It prevents ECDSA signature malleability.

        More info: https://atproto.com/specs/cryptography#ecdsa-signature-malleability
        """
        if s > self.curve_order // 2:
            raise InvalidSignature('Invalid signature. Non low-S signature variant is denied.')

    def _encode_signature(self, signature: bytes) -> bytes:
        """Encode signature."""
        r = int.from_bytes(signature[:32], 'big')
        s = int.from_bytes(signature[32:], 'big')

        self._ensure_dss_signature_low_s(s)

        return encode_dss_signature(r, s)

    def verify_signature(self, pubkey: bytes, signing_input: bytes, signature: bytes) -> bool:
        """Verify signature.

        Args:
            pubkey: Public key.
            signing_input: Signing input (data).
            signature: Signature.

        Returns:
            :obj:`bool`: True if signature is valid, False otherwise.
        """
        try:
            self.get_elliptic_curve_public_key(pubkey).verify(
                signature=self._encode_signature(signature), data=signing_input, signature_algorithm=ECDSA(SHA256())
            )
            return True
        except InvalidSignature:
            return False
