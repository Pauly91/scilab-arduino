
'''
Author : Abel Paul Babu

Class arduin

'''

import sys
from serial.tools import list_ports
from serial import Serial
from time import sleep

class arduinoCore(object):
    def __init__(self):
        self.__port = "" # initialize the port as string,
        # and __ is given so that is not accessible as instance attribute

    def __checkfirmware(self):  # This function is used to check for the firmware inside the board
        # Not sure of the logic of the implementation ->  NEED FURTHER CLARIFICATION
        self.__port.write(chr(118))
        try:
            x = self.__port.read()
            print x
            if x == 'o':
                try:
                    x = self.__port.read()
                except:
                    sys.exit("aa..! error..! it seems correct firmware not loaded")
            else:
                sys.exit("aa..! error..! it seems correct firmware not loaded")
        except:
            sys.exit("aa..! error..! it seems correct firmware not loaded")

    def locate_port(self):  # Searches for the serial port both in windows and linux -> Verified for linux
        if sys.platform.startswith('win'):
            ports = list(list_ports.comports())  # check if this works in windows
            for i in ports:
                for j in i:
                    if 'Arduino' in j:
                        self.__port = i[0]

        elif sys.platform.startswith('linux'):
            possiblePorts = []
            allPorts = list(list_ports.comports())  # list out the ports that are connected to the computer
            for i in range(len(allPorts)):
                for x in range(7):  # assuming only 7 are there
                    portName = "/dev/ttyUSB"+str(x)  # ACM for some arduino
                    if allPorts[i][0] == portName:  # Check if the following port matches with the listed port
                        possiblePorts.append(allPorts[i][0])
            if not possiblePorts:  # if no port found Exit saying no port connected
                print "Arduino Not Connected"
                sys.exit(" No serial port connected")
            self.__port = possiblePorts[0]  # If ports are found then choose the first port from the available ports
        return self.__port

    def open_serial(self, ard_no, PortNo, baudrate):
        if PortNo =='':
            sys.exit("Arduino Not Found !!")
        else:
            tempPort = Serial(PortNo, baudrate)  # assign the port to a temp Port
        with tempPort:  # This is done to reset the port if something is holding it.
            tempPort.setDTR(False)
            sleep(1)
            tempPort.flushInput()
            tempPort.setDTR(True) # with keyword closes the open port as well
        self.__port = Serial(PortNo, baudrate)  # Open the port with the port ID and the Baud rate
        sleep(2)
       # self.__checkfirmware()  # Cuurently commented out
        return self.__port

    def close_serial(self):
        self.__port.close()  # CLose the port after use

    def __del__(self):
        self.__port.close()   # A fail safe method if the user forgets to close the serial port


class digital(object):
    def __init__(self, port):
        self.__port = port  # assign the open port
        self.__selector = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "A", "B", "C", "D"]

    def cmd_digital_out(self, Ano, pin, val):
        cmd = "D"+"a"+self.__selector[pin]+"1"  # set the pin as output
        self.__port.write(cmd)  # send the command to the arduino
        cmd = "D"+"w"+self.__selector[pin]+str(val)  # val is either 0 or 1  - write high or low to the pin
        self.__port.write(cmd)  # send the command to the arduino

    def cmd_digital_in(self, Ano, pin):
        cmd = "D"+"a"+self.__selector[pin]+"0"  # set the pin as Input
        self.__port.write(cmd)   # send the command to the arduino
        cmd = "D"+"r"+self.__selector[pin]  # set the pin to read the value
        self.__port.write(cmd)  # send the command to the arduino
        result = self.__port.read()  # Read the data from the arduino
        return result


class analog(object):
    def __init__(self, port):
        self.__port = port  # assign the open port
        self.__selector = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "A", "B", "C", "D"]

    def cmd_analog_in(self, Ano, pin):
        cmd = "A"+self.__selector[pin]  # sets the pin as the input
        self.__port.write(cmd)  # send the command to the arduino
        value = self.__port.read()  # read the value from the port
        return int((1023-0)*int(ord(value))/(255-0))  # scale the value to represent on a specific scale

    def cmd_analog_out(self, Ano, pin, val):
        cmd = "W" + self.__selector[pin] + chr(val)  # Sets the pin as output and assigns the 8 bit value
        self.__port.write(cmd)  # send the command to the arduino


class ServoMotor(object):
    def __init__(self, port):
        self.__port = port  # assign the open port
        self.__selector = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "A", "B", "C", "D"]

    def cmd_servo_attach(self, Ano, servo):  # 1->pin=9  #2->pin=10  -> for __init__ ?
        cmd = "S" + "a" + self.__selector[servo]
        self.__port.write(cmd)  # send the command to the arduino

    def cmd_servo_detach(self, Ano, servo):  # 1->pin=9  #2->pin=10 descriptor ?
        cmd = "S" + "d" + self.__selector[servo]
        self.__port.write(cmd)  # send the command to the arduino

    def cmd_servo_move(self, Ano, servo, angle):  # 1->pin=9  #2->pin=10
        cmd = "S" + "w" + self.__selector[servo] + chr(angle)
        self.__port.write(cmd)  # send the command to the arduino


class DcMotor(object):
    def __init__(self, port, Ano, mode, mno, pin1, pin2):
        self.__port = port  # assign the open port
        self.__selector = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "A", "B", "C", "D"]
        self.__cmd_dcmotor_setup(Ano, mode, mno, pin1, pin2)  # initial setup

    def __cmd_dcmotor_setup(self, Ano, mode, mno, pin1, pin2):  # sets up the dc motor
        #  This method is not Accessible the object
        cmd = "C" + self.__selector[mno] + self.__selector[pin1] + self.__selector[pin2] + self.__selector[mode]
        self.__port.write(cmd)  # send the command to the arduino

    def cmd_dcmotor_run(self, Ano, mno, val):
        if val < 0:
            direction = 0
        else:
            direction = 1
        cmd = "M" + self.__selector[mno] + self.__selector[direction] + chr(abs(val))
        self.__port.write(cmd)  # send the command to the arduino

    def cmd_dcmotor_release(self, Ano, mno):  # introduce both a destructor call and an explicit call for the user.
        cmd = "M" + self.__selector[mno] + "r"
        self.__port.write(cmd)  # send the command to the arduino


def main():
    serial_port = arduinoCore()
    portNo = serial_port.locate_port()
    print portNo
    port = serial_port.open_serial(1, portNo, 9600)
    port.write("abel")
    #print type(port)
    analogFunction = DcMotor(port, 1, 1,1 , 1, 1)
    analogFunction.cmd_dcmotor_run(1,1,1)
    a = digital(port)
    a.cmd_digital_out(1,1,1)

    b = ServoMotor(port)
    b.cmd_servo_move(1,1,1)

    c = analog(port)
    c.cmd_analog_in(1,1)


if __name__ == "__main__":
    main()