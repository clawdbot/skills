import typing as t
from dataclasses import dataclass
from pathlib import Path

from atproto_core.nsid import NSID
from atproto_lexicon.models import (
    LexDefinition,
    LexDefinitionType,
    LexiconDoc,
    LexRecord,
    LexXrpcProcedure,
    LexXrpcQuery,
)
from atproto_lexicon.parser import lexicon_parse_dir

_VALID_LEX_DEF_TYPES = {LexDefinitionType.QUERY, LexDefinitionType.PROCEDURE, LexDefinitionType.RECORD}


def _filter_namespace_valid_definitions(definitions: t.Dict[str, LexDefinition]) -> t.Dict[str, LexDefinition]:
    result = {}

    for def_name, def_content in definitions.items():
        if def_content.type in _VALID_LEX_DEF_TYPES:
            result[def_name] = def_content

    return result


def get_definition_by_name(name: str, defs: t.Dict[str, LexDefinition]) -> LexDefinition:
    if name in defs:
        return defs[name]

    return defs['main']


@dataclass
class ObjectInfo:
    name: str
    nsid: NSID


@dataclass
class ProcedureInfo(ObjectInfo):
    definition: LexXrpcProcedure


@dataclass
class QueryInfo(ObjectInfo):
    definition: LexXrpcQuery


MethodInfo = t.Union[ProcedureInfo, QueryInfo]


@dataclass
class RecordInfo(ObjectInfo):
    definition: LexRecord


def _enrich_namespace_tree(root: dict, nsid: NSID, defs: t.Dict[str, LexDefinition]) -> None:
    root_node: t.Union[dict, list] = root

    segments_count = len(nsid.segments)
    for path_level, segment in enumerate(nsid.segments):
        # if method
        if path_level == segments_count - 1:
            definition = get_definition_by_name(segment, defs)

            model_class: t.Type[ObjectInfo]
            if definition.type is LexDefinitionType.PROCEDURE:
                model_class = ProcedureInfo
            elif definition.type is LexDefinitionType.QUERY:
                model_class = QueryInfo
            elif definition.type is LexDefinitionType.RECORD:
                model_class = RecordInfo
            else:
                raise RuntimeError(f'Unknown definition type: {definition.type}')

            # TODO(MarshalX): fake records as namespaces with methods to be able to reuse code of generator?

            if model_class:
                root_node.append(model_class(name=segment, nsid=nsid, definition=definition))

            continue

        if segment not in root_node:
            # if end of method's path
            if path_level == segments_count - 2:
                root_node[segment] = []
            else:
                root_node[segment] = {}
        root_node = root_node[segment]


def build_namespace_tree(lexicons: t.List[LexiconDoc]) -> dict:
    namespace_tree = {}
    for lexicon in lexicons:
        defs = _filter_namespace_valid_definitions(lexicon.defs)
        if not defs:
            continue

        nsid = NSID.from_str(lexicon.id)
        _enrich_namespace_tree(namespace_tree, nsid, defs)

    return namespace_tree


def build_namespaces(lexicon_dir: t.Optional[Path] = None) -> dict:
    lexicons = lexicon_parse_dir(lexicon_dir)
    return build_namespace_tree(lexicons)


if __name__ == '__main__':
    build_namespaces()
