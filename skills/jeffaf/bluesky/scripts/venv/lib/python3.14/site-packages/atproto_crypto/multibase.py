import libipld


def multibase_to_bytes(data: str) -> bytes:
    """Decode multibase.

    Args:
        data: Multibase encoded data.

    Returns:
        :obj:`bytes`: Decoded data.
    """
    _, data = libipld.decode_multibase(data)
    return data


def bytes_to_multibase(encoding: str, data: bytes) -> str:
    """Encode multibase.

    Note:
        Multibase table is available here: https://github.com/multiformats/multibase/blob/master/multibase.csv

    Args:
        encoding: Encoding (the character from the table).
        data: Data.

    Returns:
        :obj:`str`: Multibase encoded data.
    """
    return libipld.encode_multibase(encoding, data)
