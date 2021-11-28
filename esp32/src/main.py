import gc
import micropython
import uasyncio as asyncio

from control import Controller
from shared import client, display, panel
from utils import restart_later, sleeper
from wifi import go_online


micropython.alloc_emergency_exception_buf(100)
gc.collect()


def run():
    print("Starting main task")
    loop = asyncio.get_event_loop()
    
    display.start()
    display.text('Hello!')
    
    if not go_online():
        raise RuntimeError("Cannot connect to WiFi")
    else:
        display.text("WiFi connected")
        
    if client.start():
        display.text("MQTT connected")
    
    Controller(display=display, client=client, panel=panel)
    gc.collect()
        
    # Keep spinning!
    loop.run_forever()
    

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
    try:
        cleanup()
    except:
        pass
    restart_later()
    
