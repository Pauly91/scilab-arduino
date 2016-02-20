
import sys
from serial.tools import list_ports
from serial import Serial
from time import sleep

class arduinoCore(object):
    def __init__(self):
        self.port = ""

    def checkfirmware(self):
        self.port.write(chr(118))

        try:
            x = self.port.read()
            print x
            if x == 'o':
                try:
                    x = self.port.read()
                except:
                    sys.exit("aa..! error..! it seems correct firmware not loaded")
            else:
                sys.exit("aa..! error..! it seems correct firmware not loaded")
        except:
            sys.exit("aa..! error..! it seems correct firmware not loaded")

    def locate_port(self): # making thing as static
        if sys.platform.startswith('win'):
            ports = list(list_ports.comports())  # check if this works in windows
            for i in ports:
                for j in i:
                    if 'Arduino' in j:
                        self.port = i[0]

        elif sys.platform.startswith('linux'):
            possiblePorts = []
            allPorts = list(list_ports.comports())
            for i in range(len(allPorts)):
                for x in range(7):  # assuming only 7 are there
                    portName = "/dev/ttyUSB"+str(x)  # ACM for some arduino
                    if allPorts[i][0] == portName:
                        possiblePorts.append(allPorts[i][0])
            if not possiblePorts:
                print "Arduino Not Connected"
                return None
            self.port = possiblePorts[0]
        return self.port

    def open_serial(self, ard_no, PortNo, baudrate):
        if PortNo =='':
            sys.exit("Arduino Not Found !!")
        else:
            self.port = Serial(PortNo, baudrate)
        sleep(2)
        self.checkfirmware()

    def close_serial(self):  # As a destructor ?
        self.port.close()


class digital(object):
    def __init__(self, port):
        self.port = port
        self.a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "A", "B", "C", "D"]

    def cmd_digital_out(self, Ano, pin, val):
        cmd = "D"+"a"+self.a[pin]+"1"
        self.port.write(cmd)
        cmd = "D"+"w"+self.a[pin]+str(val)  # val is either 0 or 1
        self.port.write(cmd)

    def cmd_digital_in(self, Ano, pin):
        a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "A", "B", "C", "D"]
        cmd = "D"+"a"+a[pin]+"0"
        self.port.write(cmd)
        cmd = "D"+"r"+a[pin]
        self.port.write(cmd)
        result = self.port.read()
        return result


class analog(object):
    def __init__(self, port):
        self.port = port
        self.a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "A", "B", "C", "D"]

    def cmd_analog_in(self, Ano, pin):

        cmd = "A"+self.a[pin]
        self.port.write(cmd)
        value = self.port.read()
        return int((1023-0)*int(ord(value))/(255-0))

    def cmd_analog_out(self, Ano, pin, val):
        cmd = "W" + self.a[pin] + chr(val)
        self.port.write(cmd)


class ServoMotor(object):
    def __init__(self, port):
        self.port = port
        self.a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "A", "B", "C", "D"]

    def cmd_servo_attach(self, Ano, servo):  # 1->pin=9  #2->pin=10  -> for __init__ ?
        cmd = "S" + "a" + self.a[servo]
        self.por.write(cmd)

    def cmd_servo_detach(self, Ano, servo):  # 1->pin=9  #2->pin=10 descriptor ?
        cmd = "S" + "d" + self.a[servo]
        self.port.write(cmd)

    def cmd_servo_move(self, Ano, servo, angle): #1->pin=9  #2->pin=10
        cmd = "S" + "w" + self.a[servo] + chr(angle)
        self.port.write(cmd)


class DcMotor(object):
    def __init__(self, port, Ano, mode, mno, pin1, pin2):
        self.port = port
        self.a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "A", "B", "C", "D"]
        cmd = "C" + self.a[mno] + self.a[pin1] + self.a[pin2] + self.a[mode]
        self.port.write(cmd)

    def cmd_dcmotor_run(self, Ano, mno, val):
        if val < 0:
            direction = 0
        else:
            direction = 1
        cmd = "M" + self.a[mno] + self.a[direction] + chr(abs(val))
        self.port.write(cmd)

    def cmd_dcmotor_release(self, Ano, mno):  # release as a destructor ?
        cmd = "M" + self.a[mno] + "r"
        self.port.write(cmd)

def main():
    serial_port = arduinoCore()
    port = serial_port.locate_port()
    print port
    serial_port.open_serial(1, port, 9600)

if __name__ == "__main__":
    main()