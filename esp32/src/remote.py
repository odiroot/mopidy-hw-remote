import machine
import time
import uasyncio as asyncio

from comms import Client
from control import Controller
from drawing import Display
from utils import enable_heartbeat, enable_stopper


def main():
    loop = asyncio.get_event_loop()
    # Debug utils.
    enable_stopper()
    enable_heartbeat()

    # Prepare on-board SSD display.
    display = Display()
    display.start()
    # Establish MQTT communication.
    client = Client('mopidy/i/#', verbose=True)
    client.start()

    # The coordination logic.
    Controller(display=display, client=client)

    try:  # Main loop!
        loop.run_forever()
    except KeyboardInterrupt:
        print('Returning to REPL.')
    except RuntimeError:
        print('Forced loop stop')
    # except Exception as e:
    #     print('Unknown crash!\n%s' % e)
    #     time.sleep(10)  # Give a chance to see the outcome.
    #     machine.reset()
    finally:
        client.stop()
        display.stop()
