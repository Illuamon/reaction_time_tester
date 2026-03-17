import serial.tools.list_ports
import datetime
import tkinter as tk
from helpers import get_avg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Nastavení komunikace s arduinem
serial_inst = serial.Serial()
'''
ports = serial.tools.list_ports.comports()
list_of_ports = []

for port in ports:
    list_of_ports.append(str(port))
    print(str(port)) 
'''
# toto je potreba udelat bude to vyber z listu, list se zobrazy a uzivatel proste napise do input fieldu
serial_inst.baudrate = 9600
serial_inst.port = "COM6" # zatím je to hardcoded, ale díky bloku nahoře to později můžu předělat do vybíratelné podoby (nejspíš přímo v gui)
serial_inst.open()

messages = ["Právě se nic neděje", "Arduino testuje...", "Reakční doba: "] 

def gen_graf_single_turn(results_list):
    #tato fce generuje graf z jednoho záznamu
    results_list = list(map(float, results_list)) # radši převeď graf na floaty, může se stát že jsou to stringy
    avg = get_avg(results_list)
    global canvas
    num_of_rounds = [i for i in range(1, len(results_list) + 1)] # abych mohla udělat graf musím očíslovat kola

    # používám try except, aby když se něco pokazí nevypnul se celý program
    try:
        fig, ax = plt.subplots()
        colors = ['green' if result <= avg else 'blue' for result in results_list] # pokud je r.d. kratší než průměr tak je zelená jinak modrá

        # toto je nastavení grafu
        bars = ax.bar(num_of_rounds, results_list, color=colors) # co je sloupec (pořadí na reakční době)
        ax.bar_label(bars, padding=5) # ukaž hodnoty sloupců nad grafem
        ax.set_xticks(num_of_rounds) # osa x
        ax.set_xticklabels([str(num) for num in num_of_rounds]) # označení sloupců na ose x
        ax.set_title('Reakční doba při jednotlivých měřeních') # název grafu
        ax.set_xlabel('pořadí') # název osy x
        ax.set_ylabel('reakční doba') # název osy y

        ax.grid(axis='y', linestyle='--', alpha=0.5) # udělá linky v grafu aby byl přehlednější

        # pokud existuje jiný graf tak ho smaž
        if canvas:
            canvas.get_tk_widget().destroy()

        # nakresli nový graf
        new_canvas = FigureCanvasTkAgg(fig, master=root)
        new_canvas.draw()
        new_canvas.get_tk_widget().grid(column=1, row=0)
        globals()['canvas'] = new_canvas

    except Exception as e:
        # pokud se něco pokazilo tak zobraz chybu
        errors_text.config(text=f"Při generování grafu se něco pokazilo: {e}")

def round(serial_inst):
    # toto je hlavní funkce, musí to být takto, aby to bylo spustitelné na tlačítko
    serial_inst.write(b'start') # řekni arduino že má začít měřit

    storage_file_results = "src/results_list_storage.txt" # path k textovému souboru k ukládání dat
    end = False 
    round_results_list = []

    while end is False:
        # pokud arduino neco poslalo
        if serial_inst.in_waiting:
            packet = serial_inst.readline()
            decoded_packet = packet.decode('utf') # poslaná informace převedená do čitelné podoby
        
            if decoded_packet.startswith("<"):
                main_text.config(text=f"{messages[2]}{get_avg(round_results_list)}") #oznam výsledek (průměr) na obrazovce

                # ukládání dat do souboru
                with open(storage_file_results, "a") as file:
                    time = datetime.datetime.now()
                    file.write(f"\n{time}\n")
                    file.write(str(round_results_list))
                    file.close()

                end = True # ukonči loop

            elif decoded_packet.startswith(">"):
                pass      
            else: # zaznamenej vysledek do listu (round results list)
                round_results_list.append(decoded_packet.replace("\r\n", ""))

    # vygeneruj graf            
    gen_graf_single_turn(round_results_list)

def start_round(serial_inst):
    # tahle fce je potřeba, aby se zobrazila zpráva o tom že arduino testuje
    main_text.config(text=messages[1]) # oznam na obrazovce že arduino měří
    root.after(10, lambda: round(serial_inst)) # za chvilinku spusť hlavní fci

# nastavení tkinteru (GUI)
def_font = (12)
root = tk.Tk()
root.title("Tester reakční doby")
frame = tk.Frame(root, pady=20)
frame.grid()
canvas = None

main_text = tk.Label(frame, text=messages[0], font=def_font, padx=20, pady=15) # textové pole
errors_text = tk.Label(frame, text="", font=(10), padx=20, pady=10) # textové pole pro zobrazení případných chyb
main_text.grid(column=0, row=0)
errors_text.grid(column=0, row=2)
start_button = tk.Button(frame, text="Start", command=lambda: start_round(serial_inst), font=def_font) # tlačítko start
start_button.grid(column=0, row=1)

tk.mainloop()
