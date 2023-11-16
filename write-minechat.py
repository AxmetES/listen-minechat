import asyncio
import json

import redis.asyncio as redis

from config import settings


async def get_hash(response: str):
    body = json.loads(response.split("\n")[0])
    return body["account_hash"]


async def send_messages(reader, writer):
    value = None
    client = redis.Redis()
    while True:
        response = await reader.read(500)
        print(f"from server: {response.decode()}")
        if (
            response.decode()
            == "Hello %username%! Enter your personal hash or leave it empty to create new account.\n"
        ):
            value = await client.get("account_hash")
            if value:
                writer.write(value + b"\n")
                await writer.drain()
            else:
                writer.write(" ".encode("utf-8") + b"\n")
                await writer.drain()
        if response.decode() == "Enter preferred nickname below:\n":
            message = input("Enter preferred nickname: ")
            writer.write(message.encode("utf-8") + b"\n" + b"\n")
            await writer.drain()
        if "account_hash" in response.decode():
            account_hash = await get_hash(response.decode())
            if not value:
                await client.set("account_hash", account_hash)
            break
    while True:
        if not response:
            print("Server did not respond within the timeout. Exiting.")
            break
        else:
            message = input("Enter your message: ")
            writer.write(message.encode("utf-8") + b"\n" + b"\n")
            await writer.drain()


async def main():
    reader, writer = await asyncio.open_connection("minechat.dvmn.org", 5050)
    send_task = asyncio.create_task(send_messages(reader, writer))
    await asyncio.gather(send_task)


asyncio.run(main())
