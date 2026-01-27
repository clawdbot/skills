import re
import typing as t
from collections import abc
from copy import deepcopy

import typing_extensions as te
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from atproto_client.models.base import UnknownDict


def _convert_camel_case_to_snake_case(string: str) -> str:
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def _convert_snake_case_to_camel_case(string: str) -> str:
    s = ''.join([w.capitalize() for w in string.split('_')])
    return s[0].lower() + s[1:]


def _is_snake_case(string: str) -> bool:
    return string == _convert_camel_case_to_snake_case(string)


def _convert_to_opposite_case(string: str) -> str:
    if _is_snake_case(string):
        return _convert_snake_case_to_camel_case(string)
    return _convert_camel_case_to_snake_case(string)


class DotDict(UnknownDict):
    """Dot notation for dictionaries.

    Note:
        If the record is out of the official lexicon, it`s impossible to deserialize it to a proper data model.
        Such models will fall back to dictionaries.
        All unknown "Union" types will also be caught as dicts.
        This class exists to provide an ability to use such fallbacks as “real” data models.

    Example:
        >>> test_data = {'a': 1, 'b': {'c': 2}, 'd': [{'e': 3}, 4, 5]}
        >>> model = DotDict(test_data)
        >>> assert isinstance(model, DotDict)
        >>> assert model.nonExistingField is None
        >>> assert model.a == 1
        >>> assert model['a'] == 1
        >>> assert model['b']['c'] == 2
        >>> assert model.b.c == 2
        >>> assert model.b['c'] == 2
        >>> assert model['b'].c == 2
        >>> assert model.d[0].e == 3
        >>> assert model['d'][0]['e'] == 3
        >>> assert model['d'][0].e == 3
        >>> assert model['d'][1] == 4
        >>> assert model['d'][2] == 5
        >>> model['d'][0]['e'] = 6
        >>> assert model['d'][0]['e'] == 6
        >>> assert DotDict(test_data) == DotDict(test_data)
        >>> assert model.to_dict() == test_data
    """

    def __init__(self, data: t.Dict[str, t.Any]) -> None:
        self._data = deepcopy(data)
        for k, v in self._data.items():
            self.__setitem__(k, v)

    def to_dict(self) -> t.Dict[str, t.Any]:
        """Unwrap DotDict to Python built-in dict."""
        return deepcopy(self._data)

    def __getitem__(self, item: str) -> t.Optional[t.Any]:
        value = self._data.get(item)
        if value is not None:
            return value

        return self._data.get(_convert_to_opposite_case(item))

    __getattr__ = __getitem__

    def __setitem__(self, key: str, value: t.Any) -> None:
        if key == '_data':
            super().__setattr__(key, value)
            return

        # we store the field in case that was firstly meet to not create duplicates
        if key not in self._data and _is_snake_case(key):
            key = _convert_snake_case_to_camel_case(key)

        self._data.__setitem__(key, DotDict.__convert(value))

    __setattr__ = __setitem__

    def __iter__(self) -> t.Iterator[t.Any]:
        yield from iter(self._data)

    def keys(self) -> abc.KeysView:
        return self._data.keys()

    def values(self) -> abc.ValuesView:
        return self._data.values()

    def items(self) -> abc.ItemsView:
        return self._data.items()

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, item: t.Any) -> bool:
        return item in self._data

    def __eq__(self, other: t.Any) -> bool:
        if isinstance(other, DotDict):
            return self._data == other._data
        if isinstance(other, dict):
            return self._data == other

        raise NotImplementedError

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return repr(self._data)

    def __reduce_ex__(self, protocol: te.SupportsIndex):  # noqa: ANN204
        return self._data.__reduce_ex__(protocol)

    def __reduce__(self):  # noqa: ANN204
        return self._data.__reduce__()

    @staticmethod
    def __convert(obj: t.Any) -> t.Any:
        if isinstance(obj, dict):
            return DotDict(t.cast('t.Dict[str, t.Any]', obj))
        if isinstance(obj, list):
            return [DotDict.__convert(v) for v in t.cast('t.List[t.Any]', obj)]
        if isinstance(obj, set):
            return {DotDict.__convert(v) for v in t.cast('t.Set[t.Any]', obj)}
        if isinstance(obj, tuple):
            return tuple(DotDict.__convert(v) for v in t.cast('t.Tuple[t.Any]', obj))
        return obj


class _DotDictPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: t.Any,
        _handler: t.Callable[[t.Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        """We return a pydantic_core.CoreSchema that behaves in the following ways below.

        * dicts will be parsed as `DotDict` instances with the int as the _data attribute
        * `DotDict` instances will be parsed as `DotDict` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just a dict
        """

        def validate_from_dict(value: t.Dict[str, t.Any]) -> DotDict:
            return DotDict(value)

        from_dict_schema = core_schema.chain_schema(
            [
                core_schema.dict_schema(),
                core_schema.no_info_plain_validator_function(validate_from_dict),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_dict_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(DotDict),
                    from_dict_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda instance: instance.to_dict()),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `dict`
        return handler(core_schema.dict_schema())


DotDictType = te.Annotated[DotDict, _DotDictPydanticAnnotation]
