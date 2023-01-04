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
testcase = "../opentitan_debug/program/hex/temp.hex"
   

class opentitanIO:
    def __init__(self, in_addr_url, out_addr_url, freq, reset_cycles, test):
        self.in_url = in_addr_url
        self.out_url = out_addr_url
        self.freq = freq
        self.reset_cycles = reset_cycles
        self.direction_in = 0xFFFF
        self.direction_out = 0x0000
        """
        Read the hex pattern
        """
        self.test = test
        with open(self.test, 'r') as file:
            self.hexdata = file.readlines()
        """
        Connect the input board with chip I/O:
            C7:     CLK
            C6:     RST
            C5:     en
            C4:     spi_ss
            C3:     spi_mosi
            C2:     sel
            C1:     uart_rx_inst
            C0:     uart_rx
            D7-D0: 
        """
        self.gpio_in = GpioMpsseController()
        self.gpio_in.configure(self.in_url, direction=self.direction_in, frequency=self.freq)
        self.gpio_in.write(0x0000)
        """
        Connect the output board with chip I/O:
            C7:     uart_txen
            C6:     uart_tx
            C5-C0:
            D7-D0:  gpio[7:0]
        """
        self.gpio_out = GpioMpsseController()
        self.gpio_out.configure(self.out_url, direction=self.direction_out, frequency=self.freq)
    

    def reset(self):
        """
        initial state is 0001_0000_0000_0000 -> 0x1000 when clk = 0, rst = 0
                         1001_0000_0000_0000 -> 0x9000 when clk = 1, rst = 0
                         0101_0000_0000_0000 -> 0x5000 when clk = 0, rst = 1
                         1101_0000_0000_0000 -> 0xd000 when clk = 1, rst = 1
        """      
        for i in range(self.reset_cycles):
            self.gpio_in.write(0x1000)
            self.gpio_in.write(0x9000)
            
    def release_reset(self):
        """
        active low reset
        """
        self.gpio_in.write(0x5000)
        self.gpio_in.write(0xd000)


    def set_enable(self):
        """
        set enable signal 0111_0000_0000_0000 -> 0x7000 when clk = 0
                          1111_0000_0000_0000 -> 0xf000 when clk = 1 
        """
        while True:
            self.gpio_in.write(0x7000)
            self.gpio_in.write(0xf000)

    def write_spi(self):
        """
        Always flip clock signal when writing GPIO
        Send data when negative edge (clock = 0)
        For instance, if we want to send data 2'b11 from mosi
        The x axis is signal when sampling, y axis is gpio port
        clk   0 1 0 1 0 1 0 1 0 1 0 1
        rst   0 0 1 1 1 1 1 1 1 1 1 1
        ss    1 1 1 1 0 0 0 0 0 0 1 1
        mosi  0 0 0 0 0 0 1 1 1 1 0 0
        
        pattern is 0101_0000_0000_0000 -> 0x5000 when clk = 0, ss = 1, mosi = 0
                   1101_0000_0000_0000 -> 0xd000 when clk = 1, ss = 1, mosi = 0
                   0100_0000_0000_0000 -> 0x4000 when clk = 0, ss = 0, mosi = 0
                   1100_0000_0000_0000 -> 0xc000 when clk = 1, ss = 0, mosi = 0
                   0100_1000_0000_0000 -> 0x4800 when clk = 0, ss = 0, mosi = 1
                   1100_1000_0000_0000 -> 0xc800 when clk = 1, ss = 0, mosi = 1
        """
        for pattern in self.hexdata:
            pattern = int(pattern.strip(), 16)
            self.gpio_in.write(0x4000)
            self.gpio_in.write(0xc000)
            for i in range(31, -1, -1):
                if pattern & (0b1 << i) == 0: # mosi = 0
                    self.gpio_in.write(0x4000)
                    self.gpio_in.write(0xc000)
                else: # mosi = 1
                    self.gpio_in.write(0x4800)
                    self.gpio_in.write(0xc800)
            self.gpio_in.write(0x5000)
            self.gpio_in.write(0xd000)
        

    def write_patterns(self):
        """
        The program loading flow is as follows:
        1. active low reset the chip
        2. write input pattern with spi protocol
        3. raise enable signal to make ibex core execute the pattern in sram
        4. snoop gpio signal on the digitial storage oscillscope
        """
        self.reset()
        self.write_spi()
        self.set_enable()
        
    
ot = opentitanIO(gpio_in_addr, gpio_out_addr, 10, 10, testcase)
ot.reset()
#ot.write_patterns()
    
