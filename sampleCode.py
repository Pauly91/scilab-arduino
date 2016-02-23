
from arduinoMain import *


def main():
    serial_port = arduinoCore()
    portNo = serial_port.locate_port()
    print portNo
    port = serial_port.open_serial(1, portNo, 9600)

    Dcmotor = DcMotor(port, 1, 1,1 , 1, 1)
    Dcmotor.cmd_dcmotor_run(1, 1, 1)

    a = digital(port)
    a.cmd_digital_out(1, 1, 1)

    b = ServoMotor(port)
    b.cmd_servo_move(1, 1, 1)

    c = analog(port)
    value = c.cmd_analog_in(1, 1)


if __name__ == '__main__':
    main()
