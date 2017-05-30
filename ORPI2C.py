import fcntl
import io
import time

class ORPI2C:

    def __init__(self, address=98):
        # Set up the I2C device for reading and writing
        self.device_reader = io.open("/dev/i2c-1", "rb", buffering=0)
        fcntl.ioctl(self.device_reader, 0x703, address)
        self.device_writer = io.open("/dev/i2c-1", "wb", buffering=0)
        fcntl.ioctl(self.device_writer, 0x703, address)

    def poll(self):
        self.device_writer.write('R\00')
        time.sleep(1.5)
        
        response = self.device_reader.read(31)
        response = filter(lambda x: x != '\x00', response)

        # TODO: code cleanup
        if ord(response[0]) == 1:  # the response isn't an error
            # change MSB to 0 for all received characters except the first and get a list of characters
            char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
            # NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
            return ''.join(char_list)  # convert the char list to a string and returns it
        else:
            # TODO: error handling
            pass
