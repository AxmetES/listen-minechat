import datetime
import asyncio
import aiofiles
import configargparse


parser = configargparse.ArgumentParser(
    description="host, port, file path",
    default_config_files=["myconfig.ini"],
    add_help=False
)

parser.add_argument("--help", "-help", action="help", help="Show this help message and exit")
parser.add_argument('--host', '-h', dest='host', help="server address")
parser.add_argument('--port', '-p', dest='port', help="servers port")
parser.add_argument("--path", '-pt', dest='path', help="Path to input file")

args = parser.parse_args()


async def append_to_file(data):
    filename = args.path
    async with aiofiles.open(filename, mode='a') as file:
        now = datetime.datetime.now()
        date = now.strftime('%d.%m.%y %H:%M')
        print(data)
        if data != '\n' and data != '':
            await file.write(f'[{date}] {data}\n')


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        args.host, args.port)
    data = await reader.read(1000)
    while data:
        data = await reader.read(1000)
        await append_to_file(data.decode().strip())

    print(f'Received: {data.decode()!r}')


asyncio.run(tcp_echo_client())