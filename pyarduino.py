# -*- coding: utf-8 -*-


import sys
import serial
from serial import Serial
from serial.tools.list_ports import comports
from time import sleep

p1 = 0               # Initial Position of servo motor
p2 = 0               # Final Position of servo motor


###############################################################################

def checkfirmware():
    global ser
    ser.write(chr(118))
    try: 
        x=ser.read()
        if x=='o':
            try:
                x=ser.read()
            except:
                sys.exit("aa..! error..! it seems correct firmware not loaded")
        else:
            sys.exit("aa..! error..! it seems correct firmware not loaded")
    except:
        sys.exit("aa..! error..! it seems correct firmware not loaded")

def locateport():
    if sys.platform.startswith('win'):
        port =''
        ports = list(comports())
        for i in ports:
            for j in i:
                if 'Arduino' in j:
                    port = i[0]
    
    elif sys.platform.startswith('linux'):
        b = []
        port = ''
        ports = list(comports())
        for i in range(len(ports)):
            for x in range(7):
                portname="/dev/ttyUSB"+str(x)
                if ports[i][0]==portname:
                    b.append(ports[i][0])
        port=b[0]
    return port


def open_serial(ard_no, PortNo,baudrate):
    global ser
    if PortNo =='':
        sys.exit("aa..error..! arduino not found")
    else:
        ser = Serial(PortNo,baudrate)
    sleep(2)
    checkfirmware()
                
def close_serial():
    global ser     
    ser.close()
   
#def servo(pin,pos):
#    analogWrite(pin,pos)

def cmd_digital_out(Ano,pin,val):
    cmd=""
    a=["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","A","B","C","D"]   
    cmd="D"+"a"+a[pin]+"1"    
    ser.write(cmd)
    cmd=""
    cmd="D"+"w"+a[pin]+str(val)
    ser.write(cmd)

def cmd_digital_in(Ano,pin):
    b=[]
    cmd=""
    a=["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","A","B","C","D"]   
    cmd="D"+"a"+a[pin]+"0"    
    ser.write(cmd)
    cmd=""
    cmd="D"+"r"+a[pin]
    ser.write(cmd)
    a=ser.read()
    return(a)

###############################################################################

def cmd_analog_in(Ano,pin):
    cmd=""
    a=["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","A","B","C","D"]    
    cmd="A"+a[pin]    
    ser.write(cmd)
    a=ser.read()
    return(int((1023-0)*int(ord(a))/(255-0)))

def cmd_analog_out(Ano, pin, val):
    a=["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","A","B","C","D"]
    cmd = "W" + a[pin] + chr(val)
    ser.write(cmd)


###############################################################################

def cmd_dcmotor_setup(Ano,mode,mno,pin1,pin2):
    cmd=""
    a=["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","A","B","C","D"]  
    cmd="C"+a[mno]+a[pin1]+a[pin2]+a[mode]   
    ser.write(cmd)
 

def cmd_dcmotor_run(Ano,mno,val):
    cmd=""
    if(val <0):
        dirc=0
    else:
        dirc=1
    a=["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","A","B","C","D"]  
    cmd="M"+a[mno]+a[dirc]+chr(abs(val))  
    ser.write(cmd)
    
def cmd_dcmotor_release(Ano,mno):
    cmd=""
    a=["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","A","B","C","D"]   
    cmd="M"+a[mno]+"r"   
    ser.write(cmd)

###############################################################################
   
def cmd_servo_attach(Ano,servo): #1->pin=9  #2->pin=10
    cmd=""
    a=["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","A","B","C","D"]  
    cmd="S"+"a"+a[servo]   
    ser.write(cmd)
 
def cmd_servo_detach(Ano,servo): #1->pin=9  #2->pin=10
    cmd=""
    a=["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","A","B","C","D"]    
    cmd="S"+"d"+a[servo]   
    ser.write(cmd)

def cmd_servo_move(Ano,servo,angle): #1->pin=9  #2->pin=10
    cmd=""
    a=["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","A","B","C","D"]
    cmd="S"+"w"+a[servo]+chr(angle)   
    ser.write(cmd)
def main():
    print locateport()


if __name__ == "__main__":
    main()