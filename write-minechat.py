import logging
import asyncio
import json

import redis.asyncio as redis


logging.basicConfig(
    filename="write.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def get_hash(response: str):
    body = None
    try:
        body = json.loads(response.split("\n")[0])
    except json.JSONDecodeError as json_error:
        logging.error(f"JSON decoding error: {json_error}")
    account_hash = body["account_hash"]
    nickname = body["nickname"]
    return nickname, account_hash


async def send_messages(reader, writer):
    value = None
    client = redis.Redis()
    while True:
        try:
            response = await reader.readline(500)
        except asyncio.IncompleteReadError as incomplete_read_error:
            logging.error(f"Incomplete read error: {incomplete_read_error}")
            break
        except asyncio.CancelledError:
            logging.info("Task cancelled.")
            break
        except ConnectionError as connection_error:
            logging.error(f"Connection error: {connection_error}")
            break
        except OSError as os_error:
            logging.error(f"OS error: {os_error}")
            break
        logging.info(f"from server: {response.decode()}")
        if (
            response.decode()
            == "Hello %username%! Enter your personal hash or leave it empty to create new account.\n"
        ):
            value = await client.get("account_hash")
            if value:
                logging.info(f"to server: {response.decode()}")
                writer.write(value + b"\n")
                await writer.drain()
            else:
                logging.info(f"to server: {response.decode()}")
                writer.write(" ".encode("utf-8") + b"\n")
                await writer.drain()
        if response.decode() == "Enter preferred nickname below:\n":
            message = input("Enter preferred nickname: ")
            logging.info(f"ser info: {response.decode()}")
            writer.write(message.encode("utf-8") + b"\n" + b"\n")
            await writer.drain()
        if "account_hash" in response.decode():
            nickname, account_hash = await get_hash(response.decode())
            logging.info(f"nickname: {response.decode()}")
            if not value:
                logging.info("account_hash saved.")
                try:
                    await client.set("account_hash", account_hash)
                except redis.RedisError as redis_error:
                    logging.error(f"Redis error: {redis_error}")
                    break
    while True:
        if not response:
            logging.info("Server did not respond within the timeout. Exiting.")
            break
        else:
            message = input("Enter your message: ")
            logging.info(f"message to server: {message}")
            writer.write(message.encode("utf-8") + b"\n" + b"\n")
            await writer.drain()


async def main():
    host = "minechat.dvmn.org"
    port = 5050
    reader, writer = await asyncio.open_connection(host=host, port=port)
    logging.info(f"host: {host}, port: {port}")
    send_task = asyncio.create_task(send_messages(reader, writer))
    await asyncio.gather(send_task)


asyncio.run(main())
