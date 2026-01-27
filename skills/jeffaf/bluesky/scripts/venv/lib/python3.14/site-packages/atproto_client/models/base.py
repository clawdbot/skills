import os
import typing as t
import warnings

from pydantic import BaseModel, ConfigDict, Field, alias_generators, model_validator

from atproto_client.exceptions import ModelFieldNotFoundError


def _alias_generator(name: str) -> str:
    camel_name = alias_generators.to_camel(name)

    if camel_name.endswith('_'):
        camel_name = camel_name[:-1]

    return camel_name


class AtProtocolBase: ...


class ModelBase(BaseModel, AtProtocolBase):
    """Base class for all data classes.

    Provides square brackets [] notation to get attributes like in a dictionary.
    """

    model_config = ConfigDict(extra='allow', alias_generator=_alias_generator, populate_by_name=True, strict=True)

    def __getitem__(self, item: str) -> t.Any:
        if hasattr(self, item):
            return getattr(self, item)

        raise ModelFieldNotFoundError(f"Can't find field '{item}' in the object of type {type(self)}.")

    @model_validator(mode='after')
    def __alert_about_extra_fields(self) -> 'ModelBase':
        # used for debugging purposes because gives false positives due to the way pydantic works

        if self.model_extra and os.environ.get('ATPROTO_LEXICON_WARN', '0') == '1':
            warnings.warn(
                f'Extra fields found in the object of type {type(self)}: {self.model_extra}. '  # noqa: S608
                f'Probably you are using the old version of SDK. '
                f'Please update it using `pip install -U atproto`. '
                f'In case you are working with custom lexicon ignore this warning. '
                f'It is also possible that you are working with extended record. '
                f'To disable this warning set `ATPROTO_LEXICON_WARN` to `0` in the environment variables.',
                stacklevel=0,
            )

        return self


class ParamsModelBase(ModelBase):
    pass


class DataModelBase(ModelBase):
    pass


class ResponseModelBase(ModelBase):
    pass


class SugarResponseModelBase(ResponseModelBase):
    pass


class UnknownDict(AtProtocolBase):
    pass


class UnknownRecord(ModelBase):
    pass


class UnknownUnionModel(ModelBase):
    py_type: str = Field(alias='$type')


class RecordModelBase(UnknownRecord):
    pass
