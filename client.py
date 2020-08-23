import asyncio
from loguru import logger
import pathlib
import ssl

import certifi
import websockets

logger.add("roobet.log", rotation="10 MB")

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

async def consumer_handler(websocket, path):
    async for message in websocket:
        await consumer(message)

async def hello():
    uri = "wss://crash-gs.roobet.com/"
    async with websockets.connect(
        uri, ssl=ssl_context
    ) as websocket:
        data = await websocket.recv()
        print(f"< {data}")
        # Required setup messages
        await websocket.send(bytes.fromhex('02'))
        await websocket.send(bytes.fromhex('32'))

        while True:
          data = await websocket.recv()
          if data[0] == 4:
            logger.debug("Pot amount update (0x04)")
          elif data[0] == 5:
            logger.debug("User bet data (0x05)")
          logger.info(f"< {data}")

asyncio.get_event_loop().run_until_complete(hello())
