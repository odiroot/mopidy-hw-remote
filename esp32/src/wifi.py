import gc
import machine
import network
import time

import access


wlan = network.WLAN(network.STA_IF)
gc.collect()


def go_online():
    if wlan.isconnected():
        print("Already connected to WiFi.")
        return True
    
    wlan.active(True)
    print("Scanning for networks...")
    wlan.scan()
    wlan.connect(access.SSID, access.PASSWORD)
    print("Connecting to WiFi...")
    
    counter = 0
    while not wlan.isconnected():       
        print(".", end="")
        time.sleep(1)
        counter +=1 
        
        if counter >= 30:
            print("Could not connect.")
            return False
            
    print("Network config: ", wlan.ifconfig())
    gc.collect()
    return True
