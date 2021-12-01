import gc
import uasyncio as asyncio
from machine import Pin

from comms import Client
from panel import Panel


esp_led = Pin(2, Pin.OUT, value=1)
client = Client()


async def main():
    for i in range(3):
        print("Connection attempt:", i+1)
        try:
            await client.start()
            esp_led.value(0)
            break
        except Exception as e:
            print("Cannot connect: ", e)

    # Attach controls.
    Panel(client)

    while True:
        await asyncio.sleep(5)


gc.collect()


try:
    asyncio.run(main())
finally:
    esp_led.value(1)
    client.stop()  # Prevent LmacRxBlk:1 errors
