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
serial_inst.port = "COM6" #zatím je to hardcoded, ale díky bloku nahoře to později můžu předělat do vybíratelné podoby (nejspíš přímo v gui)
serial_inst.open()

messages = ["Právě se nic neděje", "Arduino testuje...", "Reakční doba: "] 

def round(serial_inst):
    # toto je hlavní funkce, musí to být takto, aby to bylo spustitelné na tlačítko
    serial_inst.write(b'start') #řekni arduino že má začít měřit

    storage_file_results = "src/results_list_storage.txt" #path k textovému souboru k ukládání dat
    end = False 
    round_results_list = []

    while end is False:
        #pokud arduino neco poslalo
        if serial_inst.in_waiting:
            packet = serial_inst.readline()
            decoded_packet = packet.decode('utf') #poslaná informace převedená do čitelné podoby
        
            if decoded_packet.startswith("<"):
                main_text.config(text=f"{messages[2]}{get_avg(round_results_list)}") #oznam výsledek (průměr) na obrazovce

                #ukládání dat do souboru
                with open(storage_file_results, "a") as file:
                    time = datetime.datetime.now()
                    file.write(f"\n{time}\n")
                    file.write(str(round_results_list))
                    file.close()

                end = True #ukonči loop

            elif decoded_packet.startswith(">"):
                pass      
            else: #zaznamenej vysledek do listu (round results list)
                round_results_list.append(decoded_packet.replace("\r\n", ""))

def start_round(serial_inst):
    #tahle fce je potřeba, aby se zobrazila zpráva o tom že arduino testuje
    main_text.config(text=messages[1]) #oznam na obrazovce že arduino měří
    root.after(10, lambda: round(serial_inst)) #za chvilinku spusť hlavní fci

#nastavení tkinteru (GUI)
def_font = (12)
root = tk.Tk()
root.title("Tester reakční doby")
frame = tk.Frame(root, pady=20)
frame.grid()

main_text = tk.Label(frame, text=messages[0], font=def_font, padx=20, pady=15) #textové pole
main_text.grid(column=0, row=0)
start_button = tk.Button(frame, text="Start", command=lambda: start_round(serial_inst), font=def_font) #tlačítko start
start_button.grid(column=0, row=1)

tk.mainloop()
