import serial.tools.list_ports
import datetime

#This is the part where we talk with arduino
serial_inst = serial.Serial()
'''
ports = serial.tools.list_ports.comports()
list_of_ports = []

for port in ports:
    list_of_ports.append(str(port))
    print(str(port)) 
'''

serial_inst.baudrate = 9600
serial_inst.port = "COM5" #toto se muze pozdeji zmenit, me to ale staci takto, pokud to chci nekam posilat tak je to treba zmenit na input
serial_inst.open()

round_results_list = []
storage_file_results = "src/results_list_storage.txt"

while True:
    #pokud arduino neco poslalo
    if serial_inst.in_waiting:
        packet = serial_inst.readline()
        decoded_packet = packet.decode('utf') #poslana informace do citelne podoby
        print(decoded_packet)
    
        if decoded_packet.startswith("<"):
            #pokud kolo skoncilo tak printni vysledky a taky
            #je dej do textoveho souboru abychom je mohli pozdeji pouzit
            print("-----------------------------------")
            print("konec kola, vaše výsledky: ")
            print(round_results_list)
            sum = 0
            for num in round_results_list:
                sum += num
            avg = sum / len(round_results_list)
            print(f"průměr: {avg}")

            #storing into a file
            with open(storage_file_results, "a") as file:
                time = datetime.datetime.now()
                file.write(f"\n{time}\n")
                file.write(str(round_results_list))
                file.close()

            round_results_list = []

        elif decoded_packet.startswith(">"):
            pass      
        else: #zaznamenej vysledek do listu
            round_results_list.append(decoded_packet.replace("\r\n", ""))
    

#ted je potreba realne accesnout tu txt filu a z ni ty data brat a pak je vyhodnocovat
