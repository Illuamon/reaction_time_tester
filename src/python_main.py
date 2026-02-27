import serial.tools.list_ports
import datetime
import tkinter as tk
from get_results import get_avg

#Nastavení komunikace s arduinem
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

messages = ["Právě se nic neděje", "Arduino testuje...", "Reakční doba: "]

def round(serial_inst):
    serial_inst.write(b'start') #řekni arduino že má začít měřit

    main_text.config(frame, text=messages[1]) #oznam na obrazovce že arduino měří

    storage_file_results = "src/results_list_storage.txt"
    end = False
    round_results_list = []

    while end is False:
        #pokud arduino neco poslalo
        if serial_inst.in_waiting:
            packet = serial_inst.readline()
            decoded_packet = packet.decode('utf') #poslana informace do citelne podoby
        
            if decoded_packet.startswith("<"):
                #je dej do textoveho souboru abychom je mohli pozdeji pouzit
                main_text.config(frame, text=messages[2] + get_avg(round_results_list)) #oznam výsledek (průměr)

                #ukládání dat do souboru
                with open(storage_file_results, "a") as file:
                    time = datetime.datetime.now()
                    file.write(f"\n{time}\n")
                    file.write(str(round_results_list))
                    file.close()

                round_results_list = []
                end = True

            elif decoded_packet.startswith(">"):
                pass      
            else: #zaznamenej vysledek do listu
                round_results_list.append(decoded_packet.replace("\r\n", ""))

#nastavení tkinteru (GUI)
root = tk.Tk()
root.title("Tester reakční doby")
frame = tk.Frame(root, padding=10)
frame.grid()

main_text = tk.Label(frame, text=messages[0]).grid(column=0, row=0)
start_button = tk.Button(frame, text="Start", command=lambda: round(serial_inst)).grid(column=0, row=1)


tk.mainloop()
