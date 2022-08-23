"""
Created on Tue Aug 23 2022

@author: Ming-Hung Chen

Multiple classes for controlling OpenTitan SoC I/Os through FT232H
"""

from pyftdi.gpio import GpioMpsseController

"""
GPIO Board USB addresses
"""
gpio_in_addr = "ftdi://ftdi:232h:00:ff/1"
gpio_out_addr = "ftdi://ftdi:232h:00:fe/1"

"""
TestCase name
"""
test = "../opentitan_debug/program/hex/gpio.hex"

def read_file():
    with open(test, 'r') as file:
        return file.readlines()

def setUp():
    gpio_in = GpioMpsseController()
    gpio_out = GpioMpsseController()
    gpio_in.configure(gpio_in_addr, direction=0x0000, frequency=1e6)
    gpio_out.configure(gpio_out_addr, direction=0xffff, frequency=1e6)

def set_enable(self):
    self |= (0b1 << 5)
    
def hex_to_spi():
    """
    Connect the chip I/O as follows:
    GPIO[7:0] connected to out_D[7:0]
    uart_tx connectd to out_C[7]
    uart_txen connected to out_C[6]
    CLK connected to in_C[7]
    RST connected to in_C[6]
    en connected to in_C[5]
    spi_ss connected to in_C[4]
    spi_mosi connected to in_C[3]
    sel connected to in_C[2]
    uart_rx_inst connected to in_C[1]
    uart_rx connected to in_C[0]
    """
    
    
