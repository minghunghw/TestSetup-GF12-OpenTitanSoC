"""
Created on Mon Aug 22 2022

@author: Ming-Hung Chen

Connect as following to test FT232H SPI API
"""

import time
from pyftdi.spi import SpiController

spi0_addr = "ftdi://ftdi:232h:00:ff/1"
spi1_addr = "ftdi://ftdi:232h:00:fe/1"

class SpiGpioTestCase(addr):
    """Basic test for GPIO access w/ SPI mode
       It expects the following I/O setup:
       AD4 connected t0 AC0
       AD5 connected t0 AC1
       AD6 connected t0 AC2
       AD7 connected t0 AC3
    """

    # AD0: SCLK, AD1: MOSI, AD2: MISO, AD3: /CS
    AD_OFFSET = 4
    AC_OFFSET = 8
    PIN_COUNT = 4

    def setUp(self):
        self._spi = SpiController(cs_count=1)
        self._spi.configure(addr)
        self._port = self._spi.get_port(0, freq=1E6, mode=0)
        self._io = self._spi.get_gpio()

    def test_ac_to_ad(self):
        ad_pins = ((1 << self.PIN_COUNT) - 1) << self.AD_OFFSET  # input
        ac_pins = ((1 << self.PIN_COUNT) - 1) << self.AC_OFFSET  # output
        io_pins = ad_pins | ac_pins

        def ac_to_ad(ac_output):
            ac_output &= ac_pins
            ac_output >>= self.AC_OFFSET - self.AD_OFFSET
            return ac_output & ad_pins

        self._io.set_direction(io_pins, ac_pins)
        for ac_pin in range(1 << self.PIN_COUNT):
            ac_out = ac_pin << self.AC_OFFSET
            ad_in = ac_to_ad(ac_out)
            self._io.write(ac_out)
            # random SPI exchange to ensure SPI does not change GPIO
            self._port.exchange([0x00, 0xff], 2)
            buf = self._io.read()
            self.assertEqual(buf, ad_in)
        self.assertRaises(SpiIOError, self._io.write, ad_pins)


class SpiUnalignedTestCase(addr):
    """Basic test for SPI with non 8-bit multiple transfer
       It expects the following I/O setup:
       MOSI (AD1) connected to MISO (AD2)
    """

    def setUp(self):
        self._spi = SpiController(cs_count=1)
        self._spi.configure(addr)
        self._port = self._spi.get_port(0, freq=1E6, mode=0)

    def test_invalid_write(self):
        buf = b'\xff\xff'
        self.assertRaises(ValueError, self._port.write, buf, droptail=8)

    def test_bit_write(self):
        buf = b'\x0f'
        for loop in range(7):
            self._port.write(buf, droptail=loop+1)

    def test_bytebit_write(self):
        buf = b'\xff\xff\x0f'
        for loop in range(7):
            self._port.write(buf, droptail=loop+1)

    def test_invalid_read(self):
        self.assertRaises(ValueError, self._port.read, 1, droptail=8)
        self.assertRaises(ValueError, self._port.read, 2, droptail=8)

    def test_bit_read(self):
        # make MOSI stay to low level, so MISO samples 0
        self._port.write([0x00])
        for loop in range(7):
            data = self._port.read(1, droptail=loop+1)
            self.assertEqual(len(data), 1)
        # make MOSI stay to high level, so MISO samples 1
        self._port.write([0x01])
        for loop in range(7):
            data = self._port.read(1, droptail=loop+1)
            self.assertEqual(len(data), 1)

    def test_bytebit_read(self):
        self._port.write([0x00])
        for loop in range(7):
            data = self._port.read(3, droptail=loop+1)
            self.assertEqual(len(data), 3)
            self.assertEqual(data[-1], 0)
        self._port.write([0x01])
        for loop in range(7):
            data = self._port.read(3, droptail=loop+1)
            self.assertEqual(len(data), 3)

    def test_invalid_duplex(self):
        buf = b'\xff\xff'
        self.assertRaises(ValueError, self._port.exchange, buf,
                          duplex=False, droptail=8)
        self.assertRaises(ValueError, self._port.exchange, buf,
                          duplex=False, droptail=8)
        self.assertRaises(ValueError, self._port.exchange, buf,
                          duplex=True, droptail=8)
        self.assertRaises(ValueError, self._port.exchange, buf,
                          duplex=True, droptail=8)

    def test_bit_duplex(self):
        buf = b'\xcf'
        for loop in range(7):
            data = self._port.exchange(buf, duplex=True, droptail=loop+1)
            self.assertEqual(len(data), 1)
            exp = buf[0] & ~((1<<(loop+1))-1)
            # print(f'{data[0]:08b} {exp:08b}')
            self.assertEqual(data[0], exp)

    def test_bytebit_duplex(self):
        buf = b'\xff\xcf'
        for loop in range(7):
            data = self._port.exchange(buf, duplex=True, droptail=loop+1)
            self.assertEqual(len(data), 2)
            exp = buf[-1] & ~((1<<(loop+1))-1)
            # print(f'{data[-1]:08b} {exp:08b}')
            self.assertEqual(data[0], 0xFF)
            self.assertEqual(data[-1], exp)

spi0 = SpiGpioTestCase() 
spi0.setUp(spi0_addr)
spi0.test_ac_to_ad()