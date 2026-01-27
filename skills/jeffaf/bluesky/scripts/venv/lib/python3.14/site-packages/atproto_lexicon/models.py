import typing as t

import typing_extensions as te
from pydantic import BaseModel, ConfigDict, Field

Number = t.Union[int, float]


class LexDefinitionType:
    RECORD = 'record'

    QUERY = 'query'
    PROCEDURE = 'procedure'
    SUBSCRIPTION = 'subscription'

    PARAMS = 'params'
    TOKEN = 'token'  # noqa: S105
    OBJECT = 'object'

    BLOB = 'blob'
    ARRAY = 'array'

    STRING = 'string'  # TODO(MarshalX): definitions could be primitives?


class LexPrimitiveType:
    BOOLEAN = 'boolean'
    NUMBER = 'number'
    INTEGER = 'integer'
    STRING = 'string'
    REF = 'ref'
    UNION = 'union'
    UNKNOWN = 'unknown'
    CID_LINK = 'cid-link'
    BYTES = 'bytes'


class LexBase(BaseModel):
    """Base class for all lexicon models."""

    model_config = ConfigDict(extra='forbid', populate_by_name=True, strict=True)


class LexDefinitionBase(LexBase):  # original name LexUserType
    """Base class for all lexicon definitions."""

    description: t.Optional[str] = None


class LexPrimitiveBase(LexBase):
    """Base class for all lexicon primitives."""

    description: t.Optional[str] = None


class LexXrpcError(LexBase):
    name: str
    description: t.Optional[str] = None


class LexUnknown(LexPrimitiveBase):
    type: te.Literal['unknown'] = Field(default=LexPrimitiveType.UNKNOWN, frozen=True)


class LexCidLink(LexPrimitiveBase):
    type: te.Literal['cid-link'] = Field(default=LexPrimitiveType.CID_LINK, frozen=True)


class LexBytes(LexPrimitiveBase):
    type: te.Literal['bytes'] = Field(default=LexPrimitiveType.BYTES, frozen=True)

    max_length: t.Optional[Number] = Field(default=None, alias='maxLength')
    min_length: t.Optional[Number] = Field(default=None, alias='minLength')


class LexBoolean(LexPrimitiveBase):
    type: te.Literal['boolean'] = Field(default=LexPrimitiveType.BOOLEAN, frozen=True)

    default: t.Optional[bool] = None
    const: t.Optional[bool] = None


class LexNumber(LexPrimitiveBase):
    type: te.Literal['number'] = Field(default=LexPrimitiveType.NUMBER, frozen=True)

    default: t.Optional[Number] = None
    minimum: t.Optional[Number] = None
    maximum: t.Optional[Number] = None
    enum: t.Optional[t.List[Number]] = None
    const: t.Optional[Number] = None


class LexInteger(LexPrimitiveBase):
    type: te.Literal['integer'] = Field(default=LexPrimitiveType.INTEGER, frozen=True)

    default: t.Optional[int] = None
    minimum: t.Optional[int] = None
    maximum: t.Optional[int] = None
    enum: t.Optional[t.List[int]] = None
    const: t.Optional[int] = None


class LexString(LexPrimitiveBase):
    type: te.Literal['string'] = Field(default=LexPrimitiveType.STRING, frozen=True)

    format: t.Optional[str] = None
    default: t.Optional[str] = None
    min_length: t.Optional[int] = Field(default=None, alias='minLength')
    max_length: t.Optional[int] = Field(default=None, alias='maxLength')
    min_graphemes: t.Optional[int] = Field(default=None, alias='minGraphemes')
    max_graphemes: t.Optional[int] = Field(default=None, alias='maxGraphemes')
    enum: t.Optional[t.List[str]] = None
    const: t.Optional[str] = None
    known_values: t.Optional[t.List[str]] = Field(default=None, alias='knownValues')


class LexRef(LexPrimitiveBase):
    type: te.Literal['ref'] = Field(default=LexPrimitiveType.REF, frozen=True)

    ref: str


class LexRefUnion(LexPrimitiveBase):
    type: te.Literal['union'] = Field(default=LexPrimitiveType.UNION, frozen=True)

    refs: t.List[str]
    closed: t.Optional[bool] = False


LexRefVariant = te.Annotated[t.Union[LexRef, LexRefUnion], Field(discriminator='type')]
LexPrimitive = te.Annotated[
    t.Union[
        LexUnknown,
        LexCidLink,
        LexBytes,
        LexBoolean,
        LexNumber,
        LexInteger,
        LexString,
        LexRef,
        LexRefVariant,
    ],
    Field(discriminator='type'),
]

LexLimitedScopedPrimitive = te.Annotated[
    t.Union[LexBoolean, LexInteger, LexString, LexUnknown],
    Field(discriminator='type'),
]


class LexBlob(LexDefinitionBase):
    type: te.Literal['blob'] = Field(default=LexDefinitionType.BLOB, frozen=True)

    accept: t.Optional[t.List[str]] = None
    max_size: t.Optional[Number] = Field(default=None, alias='maxSize')


class LexArray(LexDefinitionBase):
    type: te.Literal['array'] = Field(default=LexDefinitionType.ARRAY, frozen=True)

    items: t.Union[LexRefVariant, te.Annotated[t.Union[LexPrimitive, LexBlob], Field(discriminator='type')]]
    min_length: t.Optional[int] = Field(default=None, alias='minLength')
    max_length: t.Optional[int] = Field(default=None, alias='maxLength')


class LexToken(LexDefinitionBase):
    type: te.Literal['token'] = Field(default=LexDefinitionType.TOKEN, frozen=True)


class LexObject(LexDefinitionBase):
    type: te.Literal['object'] = Field(default=LexDefinitionType.OBJECT, frozen=True)

    required: t.Optional[t.List[str]] = None
    nullable: t.Optional[t.List[str]] = None
    properties: t.Dict[
        str, te.Annotated[t.Union[LexPrimitive, LexArray, LexBlob, 'LexObject'], Field(discriminator='type')]
    ]


class LexRecord(LexDefinitionBase):
    type: te.Literal['record'] = Field(default=LexDefinitionType.RECORD, frozen=True)

    key: t.Optional[str] = None
    record: LexObject


class LexXrpcParameters(LexDefinitionBase):
    type: te.Literal['params'] = Field(default=LexDefinitionType.PARAMS, frozen=True)

    required: t.Optional[t.List[str]] = None
    # FIXME(MarshalX): LexArray must be also be with limited set ot types
    properties: t.Dict[str, te.Annotated[t.Union[LexLimitedScopedPrimitive, LexArray], Field(discriminator='type')]]


class LexXrpcSubscriptionMessage(LexBase):
    description: t.Optional[str] = None
    schema_: t.Optional[te.Annotated[t.Union[LexObject, LexRefVariant], Field(discriminator='type')]] = Field(
        default=None, alias='schema'
    )


class LexXrpcBody(LexBase):
    description: t.Optional[str] = None
    encoding: t.Union[str, t.List[str]]
    schema_: t.Optional[te.Annotated[t.Union[LexObject, LexRefVariant], Field(discriminator='type')]] = Field(
        default=None, alias='schema'
    )


class LexSubscription(LexDefinitionBase):
    type: te.Literal['subscription'] = Field(default=LexDefinitionType.SUBSCRIPTION, frozen=True)

    parameters: t.Optional[LexXrpcParameters] = None
    message: t.Optional[LexXrpcSubscriptionMessage] = None
    infos: t.Optional[t.List[LexXrpcError]] = None
    errors: t.Optional[t.List[LexXrpcError]] = None


class LexXrpcQuery(LexDefinitionBase):
    type: te.Literal['query'] = Field(default=LexDefinitionType.QUERY, frozen=True)

    parameters: t.Optional[LexXrpcParameters] = None
    output: t.Optional[LexXrpcBody] = None
    errors: t.Optional[t.List[LexXrpcError]] = None


class LexXrpcProcedure(LexDefinitionBase):
    type: te.Literal['procedure'] = Field(default=LexDefinitionType.PROCEDURE, frozen=True)

    parameters: t.Optional[LexXrpcParameters] = None
    input: t.Optional[LexXrpcBody] = None
    output: t.Optional[LexXrpcBody] = None
    errors: t.Optional[t.List[LexXrpcError]] = None


LexDefinition = te.Annotated[
    t.Union[
        LexBlob,
        LexArray,
        LexToken,
        LexObject,
        LexRecord,
        LexXrpcParameters,
        LexSubscription,
        LexXrpcQuery,
        LexXrpcProcedure,
        LexString,  # actually it's primitive
    ],
    Field(discriminator='type'),
]


class LexiconDoc(LexBase):
    """Lexicon document model."""

    lexicon: int
    id: str  # NSID
    defs: t.Dict[str, LexDefinition]
    description: t.Optional[str] = None
    revision: t.Optional[int] = None
