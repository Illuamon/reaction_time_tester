import serial.tools.list_ports

#This is the part where we talk with arduino
ports = serial.tools.list_ports.comports()
serial_inst = serial.Serial()
list_of_ports = []

for port in ports:
    list_of_ports.append(str(port))
    print(str(port)) 

serial_inst.baudrate = 9600
serial_inst.port = "COM4"
serial_inst.open()

while True:
    if serial_inst.in_waiting:
        packet = serial_inst.readline()
        print(packet.decode('utf'))