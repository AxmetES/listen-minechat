import logging
import asyncio
import json
import configargparse

import redis.asyncio as redis

from config import settings
from utils import write_to_json, open_connection_contextmanager


async def get_hash(response: str):
    body = None
    try:
        body = json.loads(response.split("\n")[0])
    except json.JSONDecodeError as json_error:
        logging.error(f"JSON decoding error: {json_error}")
    account_hash = body["account_hash"]
    nickname = body["nickname"]
    return nickname, account_hash


async def authorise(nickname, client, response, writer):
    value = None
    if nickname:
        value = await client.get(nickname)
        if value:
            logging.info(
                f"to server: {response.decode()}"
            )
            writer.write(value + b"\n")
            await writer.drain()
        else:
            logging.info(f"to server: {response.decode()}")
            writer.write(" ".encode("utf-8") + b"\n")
            await writer.drain()
            print("Nickname не найдет, будет создан новый пользователь.")
            logging.exception(
                "Nickname не найдет, будет создан новый пользователь."
            )
    return value


async def register(client, response, writer, reader, value, nickname):
    if response.decode() == "Enter preferred nickname below:\n":
        logging.info(f"ser info: {response.decode()}")
        writer.write(nickname.encode("utf-8") + b"\n" + b"\n")
        await writer.drain()
    else:
        logging.info("account_hash saved.")
        if not value:
            try:
                nickname, account_hash = await get_hash(response.decode())
                value = account_hash
                print(f"Ur nickname: {nickname}")
                await write_to_json("nicknames.json", nickname, value)
                logging.info(f"nickname: {response.decode()}")
                await client.set(nickname, account_hash)
                response = await reader.readline()
                print(f"from server: {response.decode()}")
            except redis.RedisError as redis_error:
                logging.error(f"Redis error: {redis_error}")
            except Exception as error:
                logging.exception(error)
        return value


async def submit_message(response, writer):
    while True:
        if not response:
            logging.info("Server did not respond within the timeout. Exiting.")
            break
        else:
            message = input("Enter your message: ")
            logging.info(f"message to server: {message}")
            writer.write(message.encode("utf-8") + b"\n" + b"\n")
            await writer.drain()


async def send_messages(reader, writer):
    value = None
    client = redis.Redis()
    nickname = args.nickname
    while True:
        try:
            response = await reader.readline()
            print(f"from server: {response.decode()}")
        except Exception as error:
            logging.exception(error)
        logging.info(f"from server: {response.decode()}")
        if (
            response.decode()
            == "Hello %username%! Enter your personal hash or leave it empty to create new account.\n"
        ):
            value = await authorise(nickname, client, response, writer)
        else:
            value = await register(client, response, writer, reader, value, nickname)
            if value:
                break

    response = await reader.readline()
    print(f"from server: {response.decode()}")

    await submit_message(response, writer)


async def write_to_tcp_client():
    async with open_connection_contextmanager(args.host, args.port) as connection:
        reader, writer = connection
        logging.info(f"host: {args.host}, port: {args.port}")
        send_task = asyncio.create_task(send_messages(reader, writer))
        await asyncio.gather(send_task)

if __name__ == '__main__':
    logging.basicConfig(
        filename="write.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )

    parser = configargparse.ArgumentParser(
        auto_env_var_prefix="",
        description="token, nickname for login or registration.",
        default_config_files=["myconfig.ini"],
        add_help=False,
    )

    parser.add_argument(
        "--help",
        "-help",
        action="help",
        help="--host - server,\n"
             "--port - port on server,\n"
             "--nickname - nickname registered previously,\n"
             "--token - token registered previously.",
    )

    parser.add_argument(
        "--host", "-h", dest="host", default=settings.HOST, type=str, help="input server address",
    )
    parser.add_argument(
        "--port", "-p", dest="port", default=settings.PORT, type=str, help="input servers port",
    )
    parser.add_argument(
        "--nickname", "-n", dest="nickname", default=settings.NICKNAME, type=str, help="input nickname"
    )
    args = parser.parse_args()
    asyncio.run(write_to_tcp_client())
