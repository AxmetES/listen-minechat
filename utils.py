import datetime
import json
import logging
from contextlib import asynccontextmanager

import aiofiles
import asyncio


async def append_to_file(filename, data):
    try:
        async with aiofiles.open(filename, mode="a") as file:
            now = datetime.datetime.now()
            date = now.strftime("%d.%m.%y %H:%M")
            if data != "\n" and data != "":
                await file.write(f"[{date}] {data}\n")
    except OSError as e:
        logging.error(f"Error writing to file: {e}")


async def read_json_file(filename):
    try:
        async with aiofiles.open(filename, "r") as file:
            content = await file.read()
            return json.loads(content)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


async def write_to_json(filename, new_nickname, account_hash):
    existing_data = await read_json_file(filename)
    existing_data.setdefault('nickname-account_hash', []).append(f'{new_nickname} - {account_hash}')
    try:
        async with aiofiles.open(filename, "w") as file:
            await file.write(json.dumps(existing_data, indent=2))
    except OSError as e:
        logging.error(f"Error writing to file: {e}")


@asynccontextmanager
async def open_connection_contextmanager(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    try:
        yield reader, writer
    except OSError as e:
        logging.error(f"Error connecting to the server: {e}")
        return
