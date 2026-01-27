import typing as t
from dataclasses import dataclass
from datetime import datetime

if t.TYPE_CHECKING:
    from atproto_core.did_doc import DidDocument


@dataclass
class CachedDid:
    """Cached DID."""

    document: 'DidDocument'
    updated_at: datetime


@dataclass
class CachedDidResult:
    """Cached DID result."""

    did: str
    document: 'DidDocument'
    updated_at: datetime
    stale: bool
    expired: bool
