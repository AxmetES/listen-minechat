import datetime
import asyncio
import logging

import aiofiles
import configargparse


logging.basicConfig(
    filename="listen.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


parser = configargparse.ArgumentParser(
    description="host, port, file path",
    default_config_files=["myconfig.ini"],
    add_help=False,
)

parser.add_argument(
    "--help", "-help", action="help", help="Show this help message and exit"
)
parser.add_argument("--host", "-h", dest="host", help="server address")
parser.add_argument("--port", "-p", dest="port", help="servers port")
parser.add_argument("--path", "-pt", dest="path", help="Path to input file")

args = parser.parse_args()


async def append_to_file(data):
    filename = args.path
    try:
        async with aiofiles.open(filename, mode="a") as file:
            now = datetime.datetime.now()
            date = now.strftime("%d.%m.%y %H:%M")
            if data != "\n" and data != "":
                await file.write(f"[{date}] {data}\n")
    except OSError as e:
        logging.error(f"Error writing to file: {e}")


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
        await append_to_file(data.decode().strip())

    logging.info(f"Received: {data.decode()!r}")
    print(f"Received: {data.decode()!r}")


asyncio.run(tcp_echo_client())
