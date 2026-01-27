##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


from atproto_client.models import base, string_formats


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.server.checkAccountStatus`."""

    activated: bool  #: Activated.
    expected_blobs: int  #: Expected blobs.
    imported_blobs: int  #: Imported blobs.
    indexed_records: int  #: Indexed records.
    private_state_values: int  #: Private state values.
    repo_blocks: int  #: Repo blocks.
    repo_commit: string_formats.Cid  #: Repo commit.
    repo_rev: str  #: Repo rev.
    valid_did: bool  #: Valid did.
