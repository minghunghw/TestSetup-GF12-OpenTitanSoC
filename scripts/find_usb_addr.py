"""
Created on Fri Aug 19 2022

@author: Ming-Hung Chen

Checking the addresses of each bridge board
"""

import time
from pyftdi.gpio import GpioMpsseController
from pyftdi.usbtools import UsbTools

# GPIO Board USB addresses
gpio = []
gpio_addr = []
FT232H_list = UsbTools.find_all([(0x403, 0x6014)])
for i in range(len(FT232H_list)):
    gpio_addr.append("ftdi://ftdi:232h:" + hex(FT232H_list[i][0].bus)[2:].zfill(2) + ":"+hex(FT232H_list[i][0].address)[2:].zfill(2)+"/1")
    print("USB Address of the " + str(i) + " board to be checked is: " + gpio_addr[i])

for i in range(len(gpio_addr)):
    gpio.append(GpioMpsseController())
    # set all C pins to input (0), all D pins to output (1)
    # direction = C[7:0], D[7:0]
    gpio[i].configure(gpio_addr[i], direction=0x00ff, frequency=1e6)

idex = input("Which board do you want to check?")
while true:
    # Write D0 to 1
    gpio[index].write(0x0001)
    # Sleep for 1 second
    time.sleep(1)
    # Write D0 to 0
    gpio[index].write(0x0000)
    # Sleep for 1 second
    time.sleep(1)

