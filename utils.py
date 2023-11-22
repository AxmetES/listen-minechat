import datetime
import json
import logging

import aiofiles


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


async def write_to_json(filename, new_nickname):
    existing_data = await read_json_file(filename)
    existing_data.setdefault('nickname', []).append(new_nickname)
    try:
        async with aiofiles.open(filename, "w") as file:
            await file.write(json.dumps(existing_data, indent=2))
    except OSError as e:
        logging.error(f"Error writing to file: {e}")
