"""" TODO docstring."""
import serial


class GPS(object):
    """docstring for ."""

    def __init__(self, port):
        """Initialize and open an serial connection."""
        self.ser = serial.Serial()
        # self.ser.port = "/dev/ttyO%i" % (port)
        self.ser.port = "/dev/tty.usbserial-FTYKMT3K"
        self.ser.baudrate = 4800
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 2
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 1
        try:
            self.ser.open()
        except Exception, e:
            print "error al establecer comunicacion con GPS: " + str(e)
            exit()

    def reset(self):
        """Reset the device."""
        pass

    def getData(self):
        """Return the average value of 10 data read from the imu."""
        if self.ser.isOpen():
            try:
                count = 10
                latitude = 0
                longitude = 0
                while(count):
                    received_packet = self.ser.readline()
                    check_packet = received_packet[0]
                    if check_packet == '$':
                        packet = received_packet[1:]
                        packet = packet[:-2]
                        # Parse the NMEA message data field
                        data_field = packet.split(",")
                        type_message = data_field[0]
                        if type_message == 'GPGGA':
                            latitude += float(data_field[2])
                            longitude += float(data_field[4])
                    count -= 1

                return(round(latitude/10, 2), round(longitude/10, 2))

            except Exception, e1:
                print "error al establecer comunicacion con GPS: " + str(e1)
