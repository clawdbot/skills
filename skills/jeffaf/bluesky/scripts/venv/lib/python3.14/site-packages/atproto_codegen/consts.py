_DISCLAIMER_LINES = [
    "# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!",
    '# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.',
    '# This file is part of Python atproto SDK. Licenced under MIT.',
]
_MAX_DISCLAIMER_LEN = max([len(s) for s in _DISCLAIMER_LINES])
DISCLAIMER = '\n'.join(_DISCLAIMER_LINES)
DISCLAIMER = f'{"#" * _MAX_DISCLAIMER_LEN}\n{DISCLAIMER}\n{"#" * _MAX_DISCLAIMER_LEN}\n\n'

PARAMS_MODEL = 'Params'
PARAMS_DICT = 'ParamsDict'
INPUT_MODEL = 'Data'
INPUT_DICT = 'DataDict'
OUTPUT_MODEL = 'Response'
