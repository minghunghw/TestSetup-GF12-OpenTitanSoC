"""
Created on Fri Aug 19 2022

@author: Ming-Hung Chen

Multiple classes for controlling OpenTitan SoC I/Os through FT232H
"""

from pyftdi.spi import SpiController
import time
import numpy as np

"""
GPIO Board USB addresses
"""
gpio0_addr = "ftdi://ftdi:232h:00:ff/1"
gpio1_addr = "ftdi://ftdi:232h:00:fe/1"

