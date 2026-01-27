import os
import typing as t
from pathlib import Path

from pydantic_core import from_json

from atproto_lexicon import models
from atproto_lexicon.exceptions import LexiconParsingError

_PATH_TO_LEXICONS = Path(__file__).parent.parent.parent.joinpath('lexicons').absolute()
_LEXICON_FILE_EXT = '.json'

L = t.TypeVar('L')


def lexicon_parse(data: dict, model_class: t.Optional[t.Type[L]] = models.LexiconDoc) -> L:
    return model_class(**data)


def lexicon_parse_file(lexicon_path: t.Union[Path, str], *, soft_fail: bool = False) -> t.Optional[models.LexiconDoc]:
    try:
        with open(lexicon_path, encoding='UTF-8') as f:
            plain_lexicon = from_json(f.read())
            return lexicon_parse(plain_lexicon)
    except Exception as e:
        if soft_fail:
            return None

        raise LexiconParsingError("Can't parse lexicon") from e


def lexicon_parse_dir(
    lexicon_dir: t.Optional[t.Union[Path, str]] = None, *, soft_fail: bool = False
) -> t.List[models.LexiconDoc]:
    lexicon_dir_path = Path(lexicon_dir) if isinstance(lexicon_dir, str) else lexicon_dir
    if lexicon_dir_path is None:
        lexicon_dir_path = _PATH_TO_LEXICONS

    parsed_lexicons = []

    for _, _, lexicons in sorted(os.walk(lexicon_dir_path)):
        for lexicon in sorted(lexicons):
            if not lexicon.endswith(_LEXICON_FILE_EXT):
                continue

            lexicon_path = lexicon_dir_path.joinpath(lexicon)
            parsed_lexicon = lexicon_parse_file(lexicon_path, soft_fail=soft_fail)
            if parsed_lexicon:
                parsed_lexicons.append(parsed_lexicon)

    return parsed_lexicons
