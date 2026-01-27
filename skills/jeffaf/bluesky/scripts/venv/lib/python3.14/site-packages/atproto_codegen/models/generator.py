import os
import typing as t
from enum import Enum
from functools import lru_cache
from pathlib import Path

from atproto_core.nsid import NSID
from atproto_lexicon import models

from atproto_codegen.consts import (
    DISCLAIMER,
    INPUT_DICT,
    INPUT_MODEL,
    OUTPUT_MODEL,
    PARAMS_DICT,
    PARAMS_MODEL,
)
from atproto_codegen.models import builder
from atproto_codegen.record_templates import (
    RECORD_CREATE_RESPONSE_MODEL_TEMPLATE,
    RECORD_GET_RESPONSE_MODEL_TEMPLATE,
    RECORD_LIST_RESPONSE_MODEL_TEMPLATE,
)
from atproto_codegen.utils import (
    _resolve_nsid_ref,
    append_code,
    capitalize_first_symbol,
    convert_camel_case_to_snake_case,
    format_code,
    gen_description_by_camel_case_name,
    get_def_model_name,
    get_file_path_parts,
    get_import_path,
    get_record_model_name,
    join_code,
    write_code,
)
from atproto_codegen.utils import get_code_intent as _

_MODELS_OUTPUT_DIR = Path(__file__).parent.parent.parent.joinpath('atproto_client', 'models')


class ModelType(Enum):
    PARAMS = 'Parameters'
    DATA = 'Input data'
    RESPONSE = 'Output data'
    DEF = 'Definition'
    RECORD = 'Record'


class TypedDictType(Enum):
    PARAMS = 'Parameters'
    DATA = 'Input data'


def save_code(nsid: NSID, code: str) -> None:
    path_to_file = _MODELS_OUTPUT_DIR.joinpath(*get_file_path_parts(nsid))
    write_code(_MODELS_OUTPUT_DIR.joinpath(path_to_file), code)


def save_code_part(nsid: NSID, code: str) -> None:
    path_to_file = _MODELS_OUTPUT_DIR.joinpath(*get_file_path_parts(nsid))
    append_code(_MODELS_OUTPUT_DIR.joinpath(path_to_file), code)


def _get_model_imports() -> str:
    # we are using ruff with F401 autofix to delete unused imports
    lines = [
        'import typing as t',
        '',
        'import typing_extensions as te',
        'from pydantic import Field',
        '',
        'from atproto_client.models import string_formats',
        '',
        'if t.TYPE_CHECKING:',
        f'{_(1)}from atproto_client import models',
        f'{_(1)}from atproto_client.models.unknown_type import UnknownType',
        f'{_(1)}from atproto_client.models.unknown_type import UnknownInputType',
        f'{_(1)}from atproto_client.models.blob_ref import BlobRef',
        f'{_(1)}from atproto_core.cid import CIDType',
        'from atproto_client.models import base',
        '',
        '',
    ]

    return join_code(lines)


_NSID_WITH_IMPORTS = set()


def _save_code_import_if_not_exist(nsid: NSID) -> None:
    if nsid not in _NSID_WITH_IMPORTS:
        lines = [DISCLAIMER, _get_model_imports()]
        save_code(nsid, join_code(lines))
        _NSID_WITH_IMPORTS.add(nsid)


def _get_model_class_def(name: str, model_type: ModelType) -> str:
    lines: t.List[str] = []

    if model_type is ModelType.PARAMS:
        lines.append(f'class {PARAMS_MODEL}(base.ParamsModelBase):')
    elif model_type is ModelType.DATA:
        lines.append(f'class {INPUT_MODEL}(base.DataModelBase):')
    elif model_type is ModelType.RESPONSE:
        lines.append(f'class {OUTPUT_MODEL}(base.ResponseModelBase):')
    elif model_type is ModelType.RECORD:
        lines.append(f'class {get_record_model_name(name)}(base.RecordModelBase):')
    elif model_type is ModelType.DEF:
        lines.append(f'class {get_def_model_name(name)}(base.ModelBase):')

    lines.append('')

    return join_code(lines)


def _get_typeddict_class_def(name: str, model_type: TypedDictType) -> str:
    lines: t.List[str] = []

    if model_type is TypedDictType.PARAMS:
        lines.append(f'class {PARAMS_DICT}(t.TypedDict):')
    elif model_type is TypedDictType.DATA:
        lines.append(f'class {INPUT_DICT}(t.TypedDict):')

    lines.append('')

    return join_code(lines)


_LEXICON_TYPE_TO_PRIMITIVE_TYPEHINT = {
    models.LexInteger: 'int',
    models.LexBoolean: 'bool',
}


def _get_optional_typehint(type_hint: str, *, optional: bool) -> str:
    if optional:
        return f't.Optional[{type_hint}]'
    return type_hint


def _get_str_enum_typehint(nsid: NSID, field_type_def: models.LexString, *, optional: bool) -> str:
    values = field_type_def.known_values or field_type_def.enum or []

    union_type_parts = []
    for value in values:
        if '#' in value:
            # reference to literal (token)
            model_path, _ = _resolve_nsid_ref(nsid, value)
            type_ = f"'{model_path}'"
        else:
            # literal
            type_ = f"t.Literal['{value}']"

        union_type_parts.append(type_)

    # known_values is not closed enum
    closed_enum = '' if field_type_def.enum else ', str'
    return f't.Union[{", ".join(union_type_parts)}{closed_enum}]'


def _get_str_typehint(nsid: NSID, field_type_def: models.LexString, *, optional: bool) -> str:
    str_typehint = 'str'

    # Map lexicon string formats to our validator types
    if field_type_def.format:
        # Map format types to our string_formats types
        format_map = {
            'at-identifier': 'string_formats.AtIdentifier',
            'at-uri': 'string_formats.AtUri',
            'cid': 'string_formats.Cid',
            'datetime': 'string_formats.DateTime',
            'did': 'string_formats.Did',
            'handle': 'string_formats.Handle',
            'nsid': 'string_formats.Nsid',
            'tid': 'string_formats.Tid',
            'record-key': 'string_formats.RecordKey',
            'uri': 'string_formats.Uri',
            'language': 'string_formats.Language',
        }
        str_typehint = format_map.get(field_type_def.format, 'str')

    # Handle existing enum/known_values logic
    if field_type_def.known_values or field_type_def.enum:
        str_typehint = _get_str_enum_typehint(nsid, field_type_def, optional=optional)

    return _get_optional_typehint(str_typehint, optional=optional)


def _get_ref_typehint(nsid: NSID, field_type_def: models.LexRef, *, optional: bool) -> str:
    model_path, _ = _resolve_nsid_ref(nsid, field_type_def.ref)
    return _get_optional_typehint(f"'{model_path}'", optional=optional)


def _get_ref_union_typehint(nsid: NSID, field_type_def: models.LexRefUnion, *, optional: bool) -> str:
    def_names = []
    for ref in field_type_def.refs:
        import_path, _ = _resolve_nsid_ref(nsid, ref)
        def_names.append(import_path)

    if not def_names and field_type_def.closed:
        raise ValueError('The schema is invalid because union must have at least one type when it is closed')

    is_unknown_union = not def_names

    if is_unknown_union:
        # union of unknown types but it must have $type field.
        def_names.append('base.UnknownUnionModel')

    # unbelievable but it's true. If schema doesn't describe the right type in Union
    # we should fall back to the plain data
    # maybe it's for the records that have custom fields... idk
    # ref: https://github.com/bluesky-social/atproto/blob/b01e47b61730d05a780f7a42667b91ccaa192e8e/packages/lex-cli/src/codegen/lex-gen.ts#L325
    # grep by "{$type: string; [k: string]: unknown}" string
    # TODO(MarshalX): use 'base.UnknownDict' and convert to DotDict
    # append 't.Dict[str, t.Any]' to def_names  # FIXME(MarshalX): support pydantic

    def_names = ', '.join([f"'{name}'" for name in def_names])

    # For discriminated unions, optionality is handled by Optional[] wrapper, not Field(default=None)
    # Pydantic 2.12.3+ warns that default=None has no effect in union context
    # Unknown unions can't use discriminator because $type is unknown
    def_field_meta = 'Field()' if is_unknown_union else 'Field(discriminator="py_type")'

    annotated_union = f'te.Annotated[t.Union[{def_names}], {def_field_meta}]'
    return _get_optional_typehint(annotated_union, optional=optional)


def _get_model_field_typehint(  # noqa: C901
    nsid: NSID,
    field_type_def: t.Union[models.LexPrimitive, models.LexArray, models.LexBlob],
    *,
    optional: bool,
    is_input_type: bool = False,
) -> str:
    field_type = type(field_type_def)

    if field_type == models.LexUnknown:
        # unknown type is a generic response with records or any not described type in the lexicon. for example, didDoc
        if is_input_type:
            return _get_optional_typehint("'UnknownInputType'", optional=optional)
        return _get_optional_typehint("'UnknownType'", optional=optional)

    type_hint = _LEXICON_TYPE_TO_PRIMITIVE_TYPEHINT.get(field_type)
    if type_hint:
        return _get_optional_typehint(type_hint, optional=optional)

    if field_type is models.LexString:
        return _get_str_typehint(nsid, field_type_def, optional=optional)

    if field_type is models.LexArray:
        items_type_hint = _get_model_field_typehint(
            nsid, field_type_def.items, optional=False, is_input_type=is_input_type
        )
        return _get_optional_typehint(f't.List[{items_type_hint}]', optional=optional)

    if field_type is models.LexRef:
        return _get_ref_typehint(nsid, field_type_def, optional=optional)

    if field_type is models.LexRefUnion:
        return _get_ref_union_typehint(nsid, field_type_def, optional=optional)

    if field_type is models.LexCidLink:
        return _get_optional_typehint("'CIDType'", optional=optional)

    if field_type is models.LexBytes:
        # CAR file containing relevant blocks
        return _get_optional_typehint('t.Union[str, bytes]', optional=optional)

    if field_type is models.LexBlob:
        # yes, it returns blob,but actually it's blob ref here
        return _get_optional_typehint("'BlobRef'", optional=optional)

    raise ValueError(f'Unknown field type {field_type.__name__}')


def _get_model_field_value(  # noqa: C901
    field_type_def: t.Union[models.LexPrimitive, models.LexArray, models.LexBlob],
    alias_name: t.Optional[str] = None,
    *,
    optional: bool,
) -> t.Dict[str, t.Any]:
    """Generate field value and metadata.

    Returns a dict with:
        - 'value': the field value (e.g., 'None' or 'Field(...)')
        - 'needs_annotated': whether this field needs Annotated wrapper
    """
    not_set = object()

    default: t.Any = not_set
    alias: t.Union[str, not_set] = alias_name or not_set
    min_length: t.Union[int, not_set] = not_set
    max_length: t.Union[int, not_set] = not_set
    ge: t.Union[int, not_set] = not_set
    le: t.Union[int, not_set] = not_set
    frozen: t.Union[bool, not_set] = not_set

    field_type = type(field_type_def)

    # Ref and RefUnion types handle their own Field generation in the type hint
    if field_type in (models.LexRef, models.LexRefUnion):
        return {'value': '', 'needs_annotated': False}

    if field_type == models.LexInteger:
        if field_type_def.default is not None:
            default = field_type_def.default
        if field_type_def.minimum is not None:
            ge = field_type_def.minimum
        if field_type_def.maximum is not None:
            le = field_type_def.maximum
        if field_type_def.const is not None:
            frozen = field_type_def.const

    elif field_type == models.LexString:
        if field_type_def.default is not None:
            default = field_type_def.default
        if field_type_def.const is not None:
            frozen = field_type_def.const
        if field_type_def.min_length is not None:
            min_length = field_type_def.min_length
        if field_type_def.max_length is not None:
            max_length = field_type_def.max_length

    elif field_type == models.LexBoolean:
        if field_type_def.default is not None:
            default = field_type_def.default
        if field_type_def.const is not None:
            frozen = field_type_def.const

    elif field_type is models.LexArray:
        if field_type_def.min_length is not None:
            min_length = field_type_def.min_length
        if field_type_def.max_length is not None:
            max_length = field_type_def.max_length

    if default is not_set and optional:
        default = None

    field_params = {
        'default': default,
        'alias': alias,
        'min_length': min_length,
        'max_length': max_length,
        'ge': ge,
        'le': le,
        'frozen': frozen,
    }

    # Check if there are any field constraints besides default
    has_field_constraints = any(value is not not_set and name != 'default' for name, value in field_params.items())

    values = []
    only_default = default is not not_set

    for name, value in field_params.items():
        if value is not_set:
            continue

        str_value = f"'{value}'" if isinstance(value, str) else str(value)

        if name == 'default':
            default = str_value
        else:
            only_default = False

        # For optional fields with constraints, exclude default from Field to avoid pydantic warning
        if optional and has_field_constraints and name == 'default':
            continue

        values.append(f'{name}={str_value}')

    # If only default value and it's None, return simple assignment
    if only_default:
        return {'value': default, 'needs_annotated': False}

    if not values:
        return {'value': '', 'needs_annotated': False}

    field_params_str = ', '.join(values)
    # For optional fields with Field constraints, use Annotated pattern
    needs_annotated = optional and has_field_constraints
    return {'value': f'Field({field_params_str})', 'needs_annotated': needs_annotated}


def _get_req_fields_set(lex_obj: t.Union[models.LexObject, models.LexXrpcParameters]) -> set:
    required_fields = set()
    if lex_obj.required:
        required_fields = set(lex_obj.required)

    if hasattr(lex_obj, 'nullable') and lex_obj.nullable:
        # TODO(MarshalX): not 100% the same thing. think about it
        required_fields = required_fields.difference(set(lex_obj.nullable))

    return required_fields


def _add_dot_to_end_if_not_exist(description: str) -> str:
    if description[-1] not in {'.', '?', '!'}:
        description += '.'
    return description


def _get_field_docstring(
    field_name: str, field_type: t.Union[models.LexPrimitive, models.LexArray, models.LexBlob]
) -> str:
    field_desc = capitalize_first_symbol(field_type.description)
    if field_desc is None:
        field_desc = gen_description_by_camel_case_name(field_name)

    if isinstance(field_type, models.LexArray) and field_type.items.description:
        items_desc = capitalize_first_symbol(field_type.items.description)
        field_desc = f'{_add_dot_to_end_if_not_exist(field_desc)} {items_desc}'

    return _add_dot_to_end_if_not_exist(field_desc)


def _get_model_docstring(
    nsid: t.Union[str, NSID],
    lex_object: t.Union[models.LexXrpcQuery, models.LexSubscription, models.LexObject, models.LexXrpcParameters],
    model_type: ModelType,
) -> str:
    model_desc = f' {lex_object.description}' if lex_object.description else ''
    model_desc = f'{model_type.value} model for :obj:`{nsid}`.{model_desc}'
    model_desc = _add_dot_to_end_if_not_exist(model_desc)

    doc_string = [f'{_(1)}"""{model_desc}"""', '']

    return join_code(doc_string)


@lru_cache(maxsize=None)
def _get_pydantic_reserved_names() -> t.Set[str]:
    from pydantic import BaseModel

    class Model(BaseModel):
        pass

    instance = Model()

    return {name for name in dir(instance) if not name.startswith('_')}


def _is_reserved_pydantic_name(name: str) -> bool:
    return name in _get_pydantic_reserved_names()


def _get_model(
    nsid: NSID, lex_object: t.Union[models.LexObject, models.LexXrpcParameters], *, is_input_type: bool = False
) -> str:
    required_fields = _get_req_fields_set(lex_object)

    fields = []
    optional_fields = []

    for field_name, field_type_def in lex_object.properties.items():
        is_optional = field_name not in required_fields

        alias_name = None
        snake_cased_field_name = convert_camel_case_to_snake_case(field_name)

        # previously, camel cases aliases were applied to fields directly.
        # but it doesn't work well with pyright checks because of "populate_by_name"
        # that's why aliases are now implemented via alias_generator
        """
        if snake_cased_field_name != field_name:
            # make aliases for fields with camel case names
            alias_name = field_name
        """

        if _is_reserved_pydantic_name(snake_cased_field_name):
            # make aliases for fields with reserved names
            snake_cased_field_name += '_'  # add underscore to the end

            # handled in alias_generator.py
            # alias_name = field_name  # noqa: ERA001

        type_hint = _get_model_field_typehint(nsid, field_type_def, optional=is_optional, is_input_type=is_input_type)
        field_value_info = _get_model_field_value(field_type_def, alias_name, optional=is_optional)
        description = _get_field_docstring(field_name, field_type_def)

        # Handle Annotated pattern for optional fields with Field constraints
        # Skip if type hint already uses Annotated (e.g., ref unions)
        if field_value_info['needs_annotated'] and 'te.Annotated[' not in type_hint:
            # Wrap type in Annotated and add Field metadata
            type_hint = f'te.Annotated[{type_hint}, {field_value_info["value"]}]'
            value_def = ' = None'
        else:
            # Simple assignment
            if field_value_info['value']:
                value_def = f' = {field_value_info["value"]}'
            elif is_optional:
                # Optional fields without Field constraints still need = None
                value_def = ' = None'
            else:
                value_def = ''

        field_def = f'{_(1)}{snake_cased_field_name}: {type_hint}{value_def} #: {description}'

        if is_optional:
            optional_fields.append(field_def)
        else:
            fields.append(field_def)

    optional_fields.sort()
    fields.sort()

    fields.extend(optional_fields)

    fields.append('')

    return join_code(fields)


def _get_typeddict(
    nsid: NSID, lex_object: t.Union[models.LexObject, models.LexXrpcParameters], *, is_input_type: bool = False
) -> str:
    required_fields = _get_req_fields_set(lex_object)

    fields: t.List[str] = []
    optional_fields: t.List[str] = []

    for field_name, field_type_def in lex_object.properties.items():
        is_optional = field_name not in required_fields

        snake_cased_field_name = convert_camel_case_to_snake_case(field_name)

        type_hint = _get_model_field_typehint(nsid, field_type_def, optional=is_optional, is_input_type=is_input_type)
        description = _get_field_docstring(field_name, field_type_def)

        # Allow optional params to actually be omitted from the dict entirely
        type_hint_defaulting = f'te.NotRequired[{type_hint}]' if is_optional else type_hint
        field_def = f'{_(1)}{snake_cased_field_name}: {type_hint_defaulting} #: {description}'

        if is_optional:
            optional_fields.append(field_def)
        else:
            fields.append(field_def)

    optional_fields.sort()
    fields.sort()

    fields.extend(optional_fields)

    if len(fields) == 0:
        fields.append(f'{_(1)}pass')

    fields.append('')

    return join_code(fields)


def _get_model_raw_data(name: str) -> str:
    lines = [f'#: {name} raw data type.', f'{name}: te.TypeAlias = bytes\n\n']
    return join_code(lines)


def _generate_params_model(nsid: NSID, definition: t.Union[models.LexXrpcQuery, models.LexSubscription]) -> str:
    lines = [_get_model_class_def(nsid.name, ModelType.PARAMS)]

    if definition.parameters:
        lines.append(_get_model_docstring(nsid, definition.parameters, ModelType.PARAMS))
        lines.append(_get_model(nsid, definition.parameters, is_input_type=True))

    lines.append(_get_typeddict_class_def(nsid.name, TypedDictType.PARAMS))

    if definition.parameters:
        lines.append(_get_typeddict(nsid, definition.parameters, is_input_type=True))

    return join_code(lines)


def _generate_xrpc_body_model(nsid: NSID, body: models.LexXrpcBody, model_type: ModelType) -> str:
    lines = []
    if body.schema_:
        if isinstance(body.schema_, models.LexObject):
            lines.append(_get_model_class_def(nsid.name, model_type))
            lines.append(_get_model_docstring(nsid, body.schema_, model_type))
            lines.append(_get_model(nsid, body.schema_, is_input_type=(model_type is ModelType.DATA)))
        elif isinstance(body.schema_, models.LexRef):
            _, __ = _resolve_nsid_ref(nsid, body.schema_.ref)

            # here we can generate input and output model alises from the reference
            # but instead we just resolve reference inplace without intermediate model
            # maybe we will want to generate aliases in the future
            # so I leave this code here: https://github.com/MarshalX/atproto/pull/412
        else:
            raise ValueError('Wrong schema type or not implemented')
    else:
        if model_type is ModelType.DATA:
            model_name = INPUT_MODEL
        elif model_type is ModelType.RESPONSE:
            model_name = OUTPUT_MODEL
        else:
            raise ValueError('Wrong type or not implemented')

        lines.append(_get_model_raw_data(model_name))

    return join_code(lines)


def _generate_data_typedict(nsid: NSID, body: models.LexXrpcBody) -> str:
    lines: t.List[str] = []
    if isinstance(body.schema_, models.LexObject):
        lines.append(_get_typeddict_class_def(nsid.name, TypedDictType.DATA))
        lines.append(_get_typeddict(nsid, body.schema_, is_input_type=True))
    return join_code(lines)


def _generate_data_model(nsid: NSID, input_body: models.LexXrpcBody) -> str:
    return join_code(
        [_generate_xrpc_body_model(nsid, input_body, ModelType.DATA), _generate_data_typedict(nsid, input_body)]
    )


def _generate_response_model(nsid: NSID, output_body: models.LexXrpcBody) -> str:
    return _generate_xrpc_body_model(nsid, output_body, ModelType.RESPONSE)


def _generate_def_model(nsid: NSID, def_name: str, def_model: models.LexObject, model_type: ModelType) -> str:
    lines = [
        _get_model_class_def(def_name, model_type),
        _get_model_docstring(nsid, def_model, model_type),
        _get_model(nsid, def_model),
    ]

    def_type = f'{nsid}#{def_name}'
    if def_name == 'main':
        def_type = str(nsid)

    lines.append(f"{_(1)}py_type: t.Literal['{def_type}'] = Field(default='{def_type}', alias='$type', frozen=True)")
    lines.append('')

    return join_code(lines)


def _generate_def_token(nsid: NSID, def_name: str, def_model: models.LexToken) -> str:
    description = def_model.description
    if not description:
        description = gen_description_by_camel_case_name(def_name)

    lines = [
        f"{get_def_model_name(def_name)} = t.Literal['{nsid}#{def_name}'] #: {description}",
        '',
        '',
    ]
    return join_code(lines)


def _generate_def_array(nsid: NSID, def_name: str, def_model: models.LexArray) -> str:
    return f'{get_def_model_name(def_name)} = {_get_model_field_typehint(nsid, def_model, optional=False)}\n'


def _generate_def_string(nsid: NSID, def_name: str, def_model: models.LexString) -> str:
    # FIXME(MarshalX): support more fields. only known_values field is supported for now

    if not def_model.known_values and not def_model.enum:
        return ''

    type_hint = _get_str_typehint(nsid, def_model, optional=False)
    description = def_model.description
    if not description:
        description = gen_description_by_camel_case_name(def_name)

    lines = [
        f'{get_def_model_name(def_name)} = {type_hint} #: {description}',
        '',
        '',
    ]

    return join_code(lines)


def _generate_params_models(lex_db: builder.BuiltParamsModels) -> None:
    for nsid, defs in lex_db.items():
        _save_code_import_if_not_exist(nsid)

        definition = defs['main']
        if definition.parameters:
            if isinstance(definition.parameters, models.LexXrpcParameters):
                save_code_part(nsid, _generate_params_model(nsid, definition))
            else:
                # LexXrpcProcedure has parameters using another model
                raise ValueError('Wrong parameters type or not implemented')


def _generate_data_models(lex_db: builder.BuiltDataModels) -> None:
    for nsid, defs in lex_db.items():
        _save_code_import_if_not_exist(nsid)

        definition = defs['main']
        if definition.input:
            save_code_part(nsid, _generate_data_model(nsid, definition.input))


def _generate_response_models(lex_db: builder.BuiltResponseModels) -> None:
    for nsid, defs in lex_db.items():
        _save_code_import_if_not_exist(nsid)

        definition = defs['main']
        if definition.output:
            save_code_part(nsid, _generate_response_model(nsid, definition.output))


def _generate_def_models(lex_db: builder.BuiltDefModels) -> None:
    for nsid, defs in lex_db.items():
        _save_code_import_if_not_exist(nsid)

        for def_name, def_model in defs.items():
            if isinstance(def_model, models.LexToken):
                save_code_part(nsid, _generate_def_token(nsid, def_name, def_model))
            elif isinstance(def_model, models.LexString):
                save_code_part(nsid, _generate_def_string(nsid, def_name, def_model))
            elif isinstance(def_model, models.LexObject):
                save_code_part(nsid, _generate_def_model(nsid, def_name, def_model, ModelType.DEF))
            elif isinstance(def_model, models.LexArray):
                save_code_part(nsid, _generate_def_array(nsid, def_name, def_model))
            else:
                raise ValueError(f'Unhandled type {type(def_model)}')


def _generate_record_sugar_models(nsid: NSID) -> str:
    lines = []
    for model in [
        RECORD_GET_RESPONSE_MODEL_TEMPLATE,
        RECORD_LIST_RESPONSE_MODEL_TEMPLATE,
        RECORD_CREATE_RESPONSE_MODEL_TEMPLATE,
    ]:
        lines.append(model.format(record_import=get_import_path(nsid)))

    return join_code(lines)


def _generate_record_models(lex_db: builder.BuiltRecordModels) -> None:
    for nsid, defs in lex_db.items():
        _save_code_import_if_not_exist(nsid)

        for def_name, def_record in defs.items():
            if isinstance(def_record, models.LexRecord):
                # TODO(MarshalX): Process somehow def_record.key?
                save_code_part(nsid, _generate_def_model(nsid, def_name, def_record.record, ModelType.RECORD))
                save_code_part(nsid, _generate_record_sugar_models(nsid))


def _generate_record_type_database(lex_db: builder.BuiltRecordModels) -> None:
    type_conversion_lines = ['from atproto_client import models', 'RECORD_TYPE_TO_MODEL_CLASS = {']

    import_lines = [
        'import typing as t',
        'import typing_extensions as te',
        'from pydantic import Field',
        'if t.TYPE_CHECKING:',
        f'{_(4)}from atproto_client.models import base',
        f'{_(4)}from atproto_client import models',
        f'{_(4)}from atproto_client.models import dot_dict',
        '',
    ]
    unknown_record_type_hint_lines = ['UnknownRecordType: te.TypeAlias = t.Union[']
    unknown_record_type_pydantic_lines = ['UnknownRecordTypePydantic = te.Annotated[t.Union[']

    for nsid, defs in lex_db.items():
        _save_code_import_if_not_exist(nsid)

        for def_name, def_record in defs.items():
            # for now, there are records only in under "main" definition name.
            # need to rework a bit if this behavior is changed
            if isinstance(def_record, models.LexRecord):
                class_name = get_record_model_name(def_name)
                record_type = str(nsid)

                path_to_class = f'models.{get_import_path(nsid)}.{class_name}'

                type_conversion_lines.append(f"'{record_type}': {path_to_class},")

                unknown_record_type_hint_lines.append(f"{_(4)}'{path_to_class}',")
                unknown_record_type_pydantic_lines.append(f"{_(4)}'{path_to_class}',")

    type_conversion_lines.append('}')

    unknown_record_type_hint_lines.append(']')
    unknown_record_type_pydantic_lines.append('], Field(discriminator="py_type")]')
    unknown_record_type_pydantic_lines.append(
        "UnknownType: te.TypeAlias = t.Union[UnknownRecordTypePydantic, 'dot_dict.DotDictType']"
    )
    unknown_record_type_pydantic_lines.append(
        'UnknownInputType: te.TypeAlias = t.Union[UnknownType, t.Dict[str, t.Any]]'
    )
    unknown_type_lines = [*import_lines, *unknown_record_type_hint_lines, *unknown_record_type_pydantic_lines]

    write_code(_MODELS_OUTPUT_DIR.joinpath('type_conversion.py'), join_code(type_conversion_lines))
    write_code(_MODELS_OUTPUT_DIR.joinpath('unknown_type.py'), join_code(unknown_type_lines))


def _generate_init_files(root_package_path: Path) -> None:
    # One of the ways that I tried. Doesn't work well due to circular imports
    for root, dirs, files in sorted(os.walk(root_package_path)):
        root_path = Path(root)

        import_lines = []
        for dir_name in sorted(dirs):
            if dir_name.startswith('__'):
                continue

            import_parts = root_path.parts[root_path.joinpath(dir_name).parts.index(_MODELS_OUTPUT_DIR.parent.name) :]
            from_import = '.'.join(import_parts)

            if dir_name in {'app', 'com'}:
                continue

            import_lines.append(f'from {from_import} import {dir_name}')

        for file_name in sorted(files):
            if file_name.startswith('__'):
                continue

            import_parts = root_path.parts[root_path.parts.index(_MODELS_OUTPUT_DIR.parent.name) :]
            from_import = '.'.join(import_parts)

            import_lines.append(f'from atproto_client.{from_import} import {file_name[:-3]}')

        if root_path.name == 'models':
            # FIXME skip for now. should be generated too
            continue

        if root_path.name == '__pycache__':
            continue

        write_code(root_path.joinpath('__init__.py'), join_code(import_lines))


def _generate_empty_init_files(root_package_path: Path) -> None:
    for root, dirs, files in os.walk(root_package_path):
        root_path = Path(root)

        for dir_name in dirs:
            if dir_name.startswith('__'):
                continue

            if dir_name in {'app', 'com'}:
                continue

        for file_name in files:
            if file_name.startswith('__'):
                continue

        if root_path.name == 'models':
            # FIXME skip for now. should be generated too
            continue

        if root_path.name == '__pycache__':
            continue

        write_code(root_path.joinpath('__init__.py'), DISCLAIMER)


def _generate_import_aliases(root_package_path: Path) -> None:
    # is generates __init__.py file if models dir with aliases like this:
    # from atproto_client.models.app.bsky.actor import defs as AppBskyActorDefs # noqa: ERA001

    import_lines = []
    ids_db = ['class _Ids:']
    for root, __, files in sorted(os.walk(root_package_path)):
        root_path = Path(root)

        if root_path == root_package_path:
            continue

        for file in sorted(files):
            if file.startswith(('.', '__', '.pyc')):
                continue
            if '.cpython-' in file:
                continue

            import_parts = root_path.parts[root_path.parts.index(_MODELS_OUTPUT_DIR.parent.name) :]
            from_import = '.'.join(import_parts)

            nsid_parts = list(root_path.parts[root_path.parts.index('models') + 1 :])
            method_name_parts = file[:-3].split('_')
            alias_name = ''.join([p.capitalize() for p in [*nsid_parts, *method_name_parts]])

            camel_case_method_name = method_name_parts[0] + ''.join(ele.title() for ele in method_name_parts[1:])
            method_path = f'{".".join(nsid_parts)}.{camel_case_method_name}'
            ids_db.append(f"{_(1)}{alias_name}: str = '{method_path}'")

            import_lines.append(f'from {from_import} import {file[:-3]} as {alias_name}')

    import_lines.append(
        'from atproto_client.models.utils import '
        'create_strong_ref, '
        'get_model_as_dict, '
        'get_model_as_json, '
        'get_or_create, '
        'is_record_type'
    )
    import_lines.append('from atproto_client.models.models_loader import load_models')

    ids_db.append('ids = _Ids()')
    import_lines.extend(ids_db)

    import_lines.append('load_models()')

    write_code(_MODELS_OUTPUT_DIR.joinpath('__init__.py'), join_code(import_lines))


def generate_models(lexicon_dir: t.Optional[Path] = None, output_dir: t.Optional[Path] = None) -> None:
    if lexicon_dir:
        builder.lexicon_dir.set(lexicon_dir)

    if output_dir:
        # TODO(MarshalX): Temp hack for CLI. Pass output_dir everywhere.
        global _MODELS_OUTPUT_DIR
        _MODELS_OUTPUT_DIR = output_dir

    _generate_params_models(builder.build_params_models())
    _generate_data_models(builder.build_data_models())
    _generate_response_models(builder.build_response_models())
    _generate_def_models(builder.build_def_models())

    _generate_record_models(builder.build_record_models())
    _generate_record_type_database(builder.build_record_models())

    _generate_empty_init_files(_MODELS_OUTPUT_DIR)
    _generate_import_aliases(_MODELS_OUTPUT_DIR)

    format_code(_MODELS_OUTPUT_DIR)
