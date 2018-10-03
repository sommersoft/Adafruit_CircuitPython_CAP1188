# The MIT License (MIT)
#
# Copyright (c) 2018 Carter Nelson for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_cap1188.spi`
====================================================

CircuitPython SPI driver for the CAP1188 8-Key Capacitive Touch Sensor Breakout.

* Author(s): Carter Nelson

Implementation Notes
--------------------

**Hardware:**

* `CAP1188 - 8-Key Capacitive Touch Sensor Breakout <https://www.adafruit.com/product/1602>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

import adafruit_bus_device.spi_device as spi_device
from micropython import const
from adafruit_cap1188.cap1188 import CAP1188

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CAP1188.git"

# pylint: disable=bad-whitespace
CAP1188_SPI_SET_ADDR        = const(0x7D)
CAP1188_SPI_WRITE_DATA      = const(0x7E)
CAP1188_SPI_READ_DATA       = const(0x7F)
# pylint: enable=bad-whitespace

class CAP1188_SPI(CAP1188):
    """Driver for the CAP1188 connected over SPI."""
    def __init__(self, spi, cs):
        self._spi = spi_device.SPIDevice(spi, cs)
        self._buf = bytearray(4)
        super().__init__()

    def _read_register(self, address):
        """Return 8 bit value of register at address."""
        self._buf[0] = CAP1188_SPI_SET_ADDR
        self._buf[1] = address
        self._buf[2] = CAP1188_SPI_READ_DATA
        with self._spi as spi:
            spi.write_readinto(self._buf, self._buf) # pylint: disable=no-member
        return self._buf[3]

    def _write_register(self, address, value):
        """Write 8 bit value to registter at address."""
        self._buf[0] = CAP1188_SPI_SET_ADDR
        self._buf[1] = address
        self._buf[2] = CAP1188_SPI_WRITE_DATA
        self._buf[3] = value
        with self._spi as spi:
            spi.write(self._buf) # pylint: disable=no-member