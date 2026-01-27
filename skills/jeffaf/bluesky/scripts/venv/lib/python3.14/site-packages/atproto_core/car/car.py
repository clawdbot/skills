import typing as t

import libipld

from atproto_core.cid import CID
from atproto_core.exceptions import InvalidCARFile

Blocks = t.Dict[CID, dict]


class CAR:
    """CAR file."""

    def __init__(self, root: CID, blocks: Blocks) -> None:
        self._root = root
        self._blocks = blocks

    @property
    def root(self) -> CID:
        """Get root."""
        return self._root

    @property
    def blocks(self) -> Blocks:
        """Get blocks."""
        return self._blocks

    @classmethod
    def from_bytes(cls, data: bytes) -> 'CAR':
        """Decode CAR file.

        Note:
            You could pass as `data` response of `client.com.atproto.sync.get_repo`, for example.
            And other responses of methods in the `sync` namespace.

        Example:
            >>> from atproto import CAR, Client
            >>> client = Client()
            >>> client.login('my-handle', 'my-password')
            >>> repo = client.com.atproto.sync.get_repo({'did': client.me.did})
            >>> car_file = CAR.from_bytes(repo)
            >>> print(car_file.root)
            >>> print(car_file.blocks)

        Args:
            data: Content of the CAR file.

        Returns:
            :obj:`atproto.CAR`: Parsed CAR file.
        """
        header, blocks = libipld.decode_car(data)

        roots = header.get('roots')
        if isinstance(roots, list) and len(roots):
            # The first element of the CAR roots metadata array must be the CID of the most relevant Commit object.
            # For a generic export, this is the current (most recent) commit.
            # Additional CIDs may also be present in the roots array, with (for now) undefined meaning or order.
            root: CID = CID.decode(roots[0])
        else:
            raise InvalidCARFile('Invalid CAR file. Expected at least one root.')

        blocks = {CID.decode(cid): block for cid, block in blocks.items()}
        return cls(root=root, blocks=blocks)
