from cryptography.hazmat.primitives.asymmetric.ec import SECP256K1

from atproto_crypto.algs.base_alg import AlgBase
from atproto_crypto.consts import SECP256K1_CURVE_ORDER, SECP256K1_JWT_ALG


class Secp256k1(AlgBase):
    """K256 algorithm AKA secp256k1 AKA ES256K."""

    NAME = SECP256K1_JWT_ALG

    def __init__(self) -> None:
        super().__init__(SECP256K1(), SECP256K1_CURVE_ORDER)
