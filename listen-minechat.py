import asyncio
import logging
import configargparse

from utils import append_to_file


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


async def tcp_echo_client():
    filename = args.path
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
        await append_to_file(filename, data.decode().strip())

    logging.info(f"Received: {data.decode()!r}")
    print(f"Received: {data.decode()!r}")


asyncio.run(tcp_echo_client())
