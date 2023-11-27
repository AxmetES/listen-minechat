import asyncio
import logging
import os

import configargparse

from utils import append_to_file
from config import settings


logging.basicConfig(
    filename="listen.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


parser = configargparse.ArgumentParser(
    auto_env_var_prefix="",
    description="host, port, file filename",
    default_config_files=["myconfig.ini"],
    add_help=False,
)

parser.add_argument(
    "--help", "-help", action="help", help="Show this help message and exit"
)

file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), settings.FILENAME)
parser.add_argument("--host", "-h", dest="host", default=settings.HOST,  type=str, help="server address")
parser.add_argument("--port", "-p", dest="port", default=settings.PORT, type=str, help="servers port")
parser.add_argument("--filename", "-pt", dest="filename", default=file_dir, type=str, help="Path to input file")

args = parser.parse_args()


async def tcp_echo_client():
    logging.info(f"Start listening, host: {args.host}, port: {args.port}")
    try:
        reader, writer = await asyncio.open_connection(args.host, args.port)
    except OSError as e:
        logging.error(f"Error connecting to the server: {e}")
        return
    data = await reader.read(500)
    while data:
        data = await reader.read(500)
        print(data.decode())
        await append_to_file(args.filename, data.decode().strip())

    logging.info(f"Received: {data.decode()!r}")
    print(f"Received: {data.decode()!r}")


asyncio.run(tcp_echo_client())
