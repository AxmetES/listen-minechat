import logging
import asyncio
import json

import redis.asyncio as redis


logging.basicConfig(
    filename="write.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
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
            response = await reader.readline()
            print(f"from server: {response.decode()}")
        except Exception as error:
            logging.exception(error)
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
        elif response.decode() == "Enter preferred nickname below:\n":
            message = input("Enter preferred nickname: ")
            logging.info(f"ser info: {response.decode()}")
            writer.write(message.encode("utf-8") + b"\n" + b"\n")
            await writer.drain()
        else:
            try:
                assert json.loads(response.decode()) is None
                print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
                logging.exception(
                    "Неизвестный токен. Проверьте его или зарегистрируйте заново."
                )
                value = None
            except AssertionError as error:
                logging.info("account_hash saved.")
                if not value:
                    nickname, account_hash = await get_hash(response.decode())
                    logging.info(f"nickname: {response.decode()}")
                    await client.set("account_hash", account_hash)
                    response = await reader.readline()
                    print(f"from server: {response.decode()}")
                break
            except redis.RedisError as redis_error:
                logging.error(f"Redis error: {redis_error}")
            except Exception as error:
                logging.exception(error)

    response = await reader.readline()
    print(f"from server: {response.decode()}")

    while True:
        if not response:
            logging.info("Server did not respond within the timeout. Exiting.")
            break
        else:
            message = input("Enter your message: ")
            print(message)
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
