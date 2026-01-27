def __get_models_to_rebuild_set() -> set:
    from types import ModuleType

    not_rebuilt_classes = {
        'BaseModel',
        'ModelBase',
        'ParamsModelBase',
        'DataModelBase',
        'ResponseModelBase',
        'UnknownDict',
        'DotDict',
        'UnknownRecord',
        'RecordModelBase',
        'BlobRef',
        'CID',
    }

    # use a set to remove duplicates
    models_to_rebuild = set()

    from atproto_client import models

    for var_name in dir(models).copy():
        var_value = getattr(models, var_name)
        if not isinstance(var_value, ModuleType):
            continue

        for name, value in vars(var_value).items():
            if name.startswith('_') or name in not_rebuilt_classes:
                continue

            if hasattr(value, 'model_rebuild'):
                models_to_rebuild.add(value)

    return models_to_rebuild


def __rebuild_all_models() -> None:
    # load models to the scope
    from atproto_client import models  # noqa
    from atproto_client.models.unknown_type import UnknownType, UnknownInputType
    from atproto_client.models.blob_ref import BlobRef
    from atproto_client.models import dot_dict
    from atproto_core.cid import CIDType

    UnknownType, UnknownInputType, CIDType, dot_dict  # noqa: B018

    BlobRef.model_rebuild()
    for __model in __get_models_to_rebuild_set():
        __model.model_rebuild()


def __on_load() -> None:
    __rebuild_all_models()


def load_models() -> None:
    __on_load()
