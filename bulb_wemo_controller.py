import asyncio
import asyncio_mqtt as aiomqtt
import pywemo
devices = pywemo.discover_devices()

if len(devices) != 1:
    print("You don't enough devices")
    exit()


async def main():
    async with aiomqtt.Client("158.97.91.177",8883, username = "eva_cicese", password = "NQz4esJX$") as client:
        async with client.messages() as messages:
            for key in ['environment/wemo/bulb']:
                await client.subscribe(key)
            async for message in messages:
                if message.topic.matches("environment/wemo/bulb"):
                    devices[0].toggle()
                       

asyncio.run(main())
