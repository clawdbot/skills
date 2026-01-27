import typing as t
from dataclasses import dataclass

import libipld
import typing_extensions as te
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


@dataclass
class Multihash:
    code: int
    size: int
    digest: bytes


@dataclass(eq=False)
class CID:
    version: int
    codec: int
    hash: Multihash

    _stringified_form: t.Optional[str] = None
    _raw_byte_form: t.Optional[str] = None

    @classmethod
    def decode(cls, value: t.Union[str, bytes]) -> 'CID':
        cid = libipld.decode_cid(value)

        multihash = Multihash(
            code=cid['hash']['code'],
            size=cid['hash']['size'],
            digest=cid['hash']['digest'],
        )

        instance = cls(
            version=cid['version'],
            codec=cid['codec'],
            hash=multihash,
        )

        if isinstance(value, str):
            instance._stringified_form = value
        else:
            instance._raw_byte_form = value

        return instance

    def encode(self) -> str:
        if self._stringified_form is not None:
            return self._stringified_form

        self._stringified_form = libipld.encode_cid(self._raw_byte_form)
        return self._stringified_form

    def __str__(self) -> str:
        return self.encode()

    def __hash__(self) -> int:
        return hash(self.encode())

    def __eq__(self, other: t.Any) -> bool:
        if isinstance(other, str):
            return self.encode() == other

        if isinstance(other, CID):
            return self.encode() == other.encode()

        return False


class _CIDPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: t.Any,
        _handler: t.Callable[[t.Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        """We return a pydantic_core.CoreSchema that behaves in the following ways below.

        * Strings and bytes will be parsed as `CID` instances
        * `CID` instances will be parsed as `CID` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just a str
        """

        def validate_from_value(value: t.Union[str, bytes]) -> CID:
            return CID.decode(value)

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_value),
            ]
        )

        from_bytes_schema = core_schema.chain_schema(
            [
                core_schema.bytes_schema(),
                core_schema.no_info_plain_validator_function(validate_from_value),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(CID),
                    from_str_schema,
                    from_bytes_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda instance: instance.encode()),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `str`
        return handler(core_schema.str_schema())


CIDType = te.Annotated[CID, _CIDPydanticAnnotation]
