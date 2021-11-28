import machine
import time
    

def restart_later(delay=5):
    print(f"Will reboot in {delay}...")
    time.sleep(delay)
    machine.soft_reset()


async def sleeper():
    while True:
        asyncio.sleep(1)
