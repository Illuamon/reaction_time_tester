import serial.tools.list_ports

serial_inst = serial.Serial()
ports = serial.tools.list_ports.comports()
list_of_ports = []

for port in ports:
    list_of_ports.append(str(port))
    print(str(port)) 