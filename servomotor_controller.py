import asyncio
import asyncio_mqtt as aiomqtt
import serial


neck = serial.Serial('/dev/ttyUSB0', 9600)

async def main():
    async with aiomqtt.Client("158.97.91.177",8883, username = "eva_cicese", password = "NQz4esJX$") as client:
        async with client.messages() as messages:
            for key in ['eva/neck/animation']:
                await client.subscribe(key)
            async for message in messages:
                if message.topic.matches("eva/neck/animation"):
                       print(message.payload)
                       neck.write(message.payload)

asyncio.run(main())
