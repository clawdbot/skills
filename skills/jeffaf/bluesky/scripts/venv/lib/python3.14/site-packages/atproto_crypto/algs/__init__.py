import typing as t

from .p256 import P256
from .secp256k1 import Secp256k1

_ANY_ALG_TYPE = t.Union[t.Type[P256], t.Type[Secp256k1]]

AVAILABLE_ALGORITHMS: t.List[_ANY_ALG_TYPE] = [P256, Secp256k1]
ALGORITHM_TO_CLASS: t.Dict[str, _ANY_ALG_TYPE] = {alg.NAME: alg for alg in AVAILABLE_ALGORITHMS}

__all__ = ['ALGORITHM_TO_CLASS', 'P256', 'Secp256k1']
