"""
Portions of this code are modifed from sample code available at
https://github.com/AtlasScientific/Raspberry-Pi-sample-code.git
under the following license:

--------
The MIT License (MIT)

Copyright (c) 2016 AtlasScientific

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
--------

Last modified 03 June 2017.

See https://www.atlas-scientific.com/_files/_datasheets/_circuit/orp_EZO_datasheet.pdf
for more information about the i2c commands for this device.
"""

import fcntl
import io
import time

class Probe:
    def __init__(self, address=98):
        """Set up this device for i2c communications."""
        self.i2c_reader = io.open("/dev/i2c-1", "rb", buffering=0)
        self.i2c_writer = io.open("/dev/i2c-1", "wb", buffering=0)
        self.set_i2c_address(address)
        self.isSleeping = False

    def calibrate(self, value):
        """Calibrate the device to the given value."""
        self.i2c_writer.write('Cal,' + str(value) + '\00')
        time.sleep(1.5)  # 'Cal,nnn' command requires >900ms timeout for response

    def clear_calibration(self):
        """Clear the current calibration."""
        self.i2c_writer.write('Cal,clear\00')
        time.sleep(0.5)  # 'Cal,clear' command requires 300ms timeout for response

    def get_calibration_state(self):
        """Get the current calibration state.

        The response will be in the format '?CAL,n' where
        1 = calibrated and 0 = not calibrated.
        """
        value = self.i2c_writer.write('CAL,?\00')
        time.sleep(0.5)  # 'Cal,?' command requires 300ms timeout for response
        return self.read()

    def get_device_info(self):
        """Get device information.

        The response will be in the format '?I,<device>,<firmware>'.
        """
        self.i2c_writer.write('i\00')
        time.sleep(0.5)  # 'i' command requires 300ms timeout for response
        return self.read()

    def get_device_status(self):
        """Get device status. If the device is sleeping this status will be invalid.

        This response will be in the format '?STATUS,<restart code>,<voltage>'
        where the restart code (reason for restart) will be one of the following:
        P - powered off
        S - software reset
        B - brown out
        W - watchdog
        U - unknown
        """
        self.i2c_writer.write('Status\00')
        time.sleep(0.5)  # 'Status' command requires 300ms timeout for response
        return self.read()

    def get_i2c_address(self):
        """Get the current i2c address for this device."""
        return self.i2c_address

    def set_i2c_address(self, address):
        """Set up i2c communications with the given address."""
        I2C_SLAVE = 0x703
	fcntl.ioctl(self.i2c_reader, I2C_SLAVE, address)
	fcntl.ioctl(self.i2c_writer, I2C_SLAVE, address)
        self.i2c_address = address

    def poll(self):
        """Get a reading from the device."""
        self.i2c_writer.write('R\00')
        time.sleep(1.5)  # 'R' command requires >900ms timeout for response
        return self.read()

    def read(self, num_bytes=31):
	"""Read a specified number of bytes from I2C and return as a string.

	To get a voltage reading, use poll().
	"""
	try:
            response = self.i2c_reader.read(num_bytes)
            response = filter(lambda x: x != '\x00', response) # remove null chars
                
            # Get a list of received characters to return
            if ord(response[0]) == 1:
                # On the Raspberry Pi the MSB needs to be changed to 0 for all
                # received chars except the first
                char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
                return ''.join(char_list)
            else:
                # The response was an error
                return 'Error'
        except IOError:
            return 'Input/output error'

    def sleep(self):
        """Put the device into a low-power sleep mode.

        Any command will wake the device but will cause an IOError.
        Use wake() to wake the device and catch the error.
        """
        self.isSleeping = True
        self.i2c_writer.write('Sleep')

    def wake(self):
        """Write a command to wake the device."""
        try:
            self.isSleeping = False
            self.i2c_writer.write('i\00')
        except IOError:
            # This is expected, do nothing
            pass


