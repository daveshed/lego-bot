import logging

_LOGGER = logging.getLogger("FOO")

PORT = None

def reverseByteOrder(data):
    """Reverses the byte order of an int (16-bit) or long (32-bit) value."""
    # Courtesy Vishal Sapre
    byteCount = len(hex(data)[2:].replace('L','')[::2])
    val       = 0
    for i in range(byteCount):
        val    = (val << 8) | (data & 0xff)
        data >>= 8
    return val

def get_default_bus():
    raise NotImplementedError

def get_i2c_device(address, busnum=None, i2c_interface=None, **kwargs):
    """Return an I2C device for the specified address and on the specified bus.
    If busnum isn't specified, the default I2C bus for the platform will attempt
    to be detected.
    """
    return Device(PORT)


def require_repeated_start():
    """Enable repeated start conditions for I2C register reads.  This is the
    normal behavior for I2C, however on some platforms like the Raspberry Pi
    there are bugs which disable repeated starts unless explicitly enabled with
    this function.  See this thread for more details:
      http://www.raspberrypi.org/forums/viewtopic.php?f=44&t=15840
    """
    raise NotImplementedError


class Device:
    """Class for communicating with an I2C device using the adafruit-pureio pure
    python smbus library, or other smbus compatible I2C interface. Allows reading
    and writing 8-bit, 16-bit, and byte array values to registers
    on the device."""
    def __init__(self, port):
        self._port = port
        _LOGGER.info("Created an i2c device on %r", port)

    def writeRaw8(self, value):
        """Write an 8-bit value on the bus (without register)."""
        raise NotImplementedError

    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""
        value = value & 0xFF
        self._port.write_to(register, value.to_bytes(length=1, byteorder='big'))
        _LOGGER.debug("Wrote 0x%02X to register 0x%02X",
                     value, register)

    def write16(self, register, value):
        """Write a 16-bit value to the specified register."""
        raise NotImplementedError

    def writeList(self, register, data):
        """Write bytes to the specified register."""
        raise NotImplementedError

    def readList(self, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        raise NotImplementedError

    def readRaw8(self):
        """Read an 8-bit value on the bus (without register)."""
        raise NotImplementedError

    def readU8(self, register):
        """Read an unsigned byte from the specified register."""
        raw_data = self._port.read_from(register, 1)
        result = int.from_bytes(raw_data, byteorder='big') & 0xFF
        _LOGGER.debug("Read 0x%02X from register 0x%02X",
                     result, register)
        return result

    def readS8(self, register):
        """Read a signed byte from the specified register."""
        result = self.readU8(register)
        if result > 127:
            result -= 256
        return result

    def readU16(self, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        raise NotImplementedError

    def readS16(self, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        raise NotImplementedError

    def readU16LE(self, register):
        """Read an unsigned 16-bit value from the specified register, in little
        endian byte order."""
        raise NotImplementedError

    def readU16BE(self, register):
        """Read an unsigned 16-bit value from the specified register, in big
        endian byte order."""
        raise NotImplementedError

    def readS16LE(self, register):
        """Read a signed 16-bit value from the specified register, in little
        endian byte order."""
        raise NotImplementedError

    def readS16BE(self, register):
        """Read a signed 16-bit value from the specified register, in big
        endian byte order."""
        raise NotImplementedError
