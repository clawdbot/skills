import re
from pathlib import Path

from atproto_codegen.consts import DISCLAIMER
from atproto_codegen.utils import format_code, write_code

_CLIENT_DIR = Path(__file__).parent.parent.parent.joinpath('atproto_client', 'client')


def gen_client(input_filename: str, output_filename: str) -> None:
    with open(_CLIENT_DIR.joinpath(input_filename), encoding='UTF-8') as f:
        code = f.read()

    # TODO(MarshalX): Get automatically
    methods = [
        'send_post',
        'send_image',
        'send_images',
        'upload_blob',
        '_set_session',
        '_get_and_set_session',
        '_refresh_and_set_session',
        '_import_session_string',
        '_call_on_session_change_callbacks',
        '_invoke',
    ]

    code = code.replace('from threading', 'import asyncio\nfrom asyncio')
    code = code.replace('client.raw', 'client.async_raw')
    code = code.replace('class Client', 'class AsyncClient')
    code = code.replace('ClientRaw', 'AsyncClientRaw')
    code = code.replace('SessionDispatchMixin', 'AsyncSessionDispatchMixin')

    code = code.replace('with self', 'async with self')

    code = code.replace('def', 'async def')
    code = code.replace('async def __', 'def __')

    code = code.replace('self.com', 'await self.com')
    code = code.replace('self.app', 'await self.app')

    for method in methods:
        # TODO(MarshalX): abnormally hacky; rework
        code = re.sub(rf'(\[self\.{method}.*\])', r'await asyncio.gather(*\1)', code)

        code = code.replace(f'self.{method}(', f'await self.{method}(')
        code = code.replace(f'super().{method}(', f'await super().{method}(')

        code = code.replace('gather(*[await', 'gather(*[')  # rollback specific case

    code = DISCLAIMER + code

    write_code(_CLIENT_DIR.joinpath(output_filename), code)
    format_code(_CLIENT_DIR.joinpath(output_filename))
