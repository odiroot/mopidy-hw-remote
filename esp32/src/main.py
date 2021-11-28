import gc
import micropython
import uasyncio as asyncio

from shared import client, display
from utils import restart_later, sleeper
from wifi import go_online


micropython.alloc_emergency_exception_buf(100)
gc.collect()


def run():
    print("Starting main task")
    display.start()
    display.text('Hello!')
    
    if not go_online():
        raise RuntimeError("Cannot connect to WiFi")
    else:
        display.text("WiFi connected")
        
    if client.start():
        display.text("MQTT connected")
    
    gc.collect()
    # Keep spinning!
    asyncio.run(sleeper())
    

def cleanup():
    print("Cleanup")
    client.stop()
    display.stop()

try:
    run()
except Exception as e:
    print("Exception: ", e)
    display.text("Crash. Will restart.")
    raise e  # For console debugging.
finally:
    cleanup()
    restart_later()
    
