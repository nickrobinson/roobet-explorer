import asyncio
import pathlib
import ssl
import websockets
import certifi


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
        await websocket.send(bytes.fromhex('02'))
        await websocket.send(bytes.fromhex('32'))

        while True:
          data = await websocket.recv()
          if data[0] == 4:
            print(data[3])
            print(data[4])
          print(f"< {data}")

asyncio.get_event_loop().run_until_complete(hello())