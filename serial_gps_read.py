"""TODO."""

import serial

ser = serial.Serial()
ser.port = "/dev/ttyO4"
ser.baudrate = 4800
ser.bytesize = serial.EIGHTBITS                    # number of bits per bytes
ser.parity = serial.PARITY_NONE                    # set parity: no parity
ser.stopbits = serial.STOPBITS_ONE                 # number of stop bits
ser.timeout = None                                 # block read
ser.xonxoff = False                                # off software flow control
ser.rtscts = False                                 # off hardware (RTS/CTS)
ser.dsrdtr = False                                 # off hardware (DSR/DTR)

try:
    ser.open()
    file = open("gps_data.txt", "w")

except Exception, e:
    print "error open serial port: " + str(e)
    exit()

if ser.isOpen():

    try:
        ser.flushInput()
        while(True):
            received_packet = ser.readline()
            check_packet = received_packet[0]
            if check_packet == '$':
                packet = received_packet[1:]
                packet = packet[:-2]
                print(packet)
                # Parse the NMEA message data field
                data_field = packet.split(",")
                type_message = data_field[0]
                if type_message == 'GPGGA':
                    latitude = data_field[2]
                    longitude = data_field[4]
                    coordinates = "%s,%s\n" % (latitude, longitude)
                    file.write(coordinates)
        file.close()
        ser.close()
    except Exception, e1:
        print "error communicating...: " + str(e1)

else:
    print "cannot open serial port "
