"""TODO docstring."""

import serial
import time


class gsm(object):
    """TODO docstring."""

    def __init__(self, port):
        """Initialize and open an serial connection."""
        self.input_buffer = ""
        self.serial_port = serial.Serial()
        self.serial_port.port = "/dev/%s" % (port)
        self.serial_port.baudrate = 115200
        self.serial_port.bytesize = serial.EIGHTBITS
        self.serial_port.parity = serial.PARITY_NONE
        self.serial_port.stopbits = serial.STOPBITS_ONE
        self.serial_port.timeout = 2
        self.serial_port.xonxoff = False
        self.serial_port.rtscts = False
        self.serial_port.dsrdtr = False
        self.serial_port.writeTimeout = 1
        try:
            self.serial_port.open()
        except Exception, e:
            print "error al establecer comunicacion con sensores \
                   ambientales: " + str(e)
            exit()

    def modemState(self):
        """TODO docstring."""
        self.serial_port.reset_input_buffer()
        time.sleep(100e-3)
        self.serial_port.write('AT\r')
        timeout = time.time() + 1
        while True:
            read_buffer = self.serial_port.read()
            self.input_buffer = self.input_buffer + read_buffer.decode('ascii')
            if '\r' in self.input_buffer:
                received_packet = self.input_buffer[:-1]
                self.input_buffer = ""
                return str(received_packet)
            if time.time() > timeout:
                return -1
            time.sleep(10e-3)

    def resetModem(self):
        """TODO docstring."""
        self.serial_port.write('ATZ\r')
        time.sleep(2)   # validate time to wait for reset modem.

    def sendMessage(self, number, text):
        """TODO docstring."""
        self.serial_port.write('''AT+CMGS="''' + number + '''"\r''')
        time.sleep(1)
        self.serial_port.write(text + "\r")
        time.sleep(1)
        self.serial_port.write(chr(26))
        time.sleep(2)

    def enableTextMode(self):
        """TODO docstring."""
        self.serial_port.write('AT+CMGF=1\r')
        time.sleep(1)

    def setCharacterSet(self):
        """TODO docstring."""
        self.serial_port.write('AT+CSCS="GSM"\r')
        time.sleep(1)

    def signalQuality(self):
        """TODO docstring."""
        self.serial_port.reset_input_buffer()
        self.serial_port.write('AT+CSQ\r')
        time.sleep(2)
        timeout = time.time() + 1
        while True:
            read_buffer = self.serial_port.read()
            self.input_buffer = self.input_buffer + read_buffer.decode('ascii')
            if '\r' in self.input_buffer:
                received_packet = self.input_buffer[:-1]
                self.input_buffer = ""
                return str(received_packet)
            if time.time() > timeout:
                return -1
            time.sleep(10e-3)
