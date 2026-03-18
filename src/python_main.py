import serial.tools.list_ports
import datetime
import tkinter as tk
from helpers import get_avg, get_list_from_line, get_all_time_avg
import matplotlib.pyplot as plt
from settings import SERIAL_PORT, RESULTS_STRG_PATH
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Nastavení komunikace s arduinem
serial_inst = serial.Serial()

# toto je potreba udelat bude to vyber z listu, list se zobrazy a uzivatel proste napise do input fieldu
serial_inst.baudrate = 9600
serial_inst.port = SERIAL_PORT # dá se předělat v settings.py 
serial_inst.open()

messages = ["Právě se nic neděje", "Arduino testuje...", "Reakční doba: ", "Průměrná reakční doba ze všech záznamů: "] 

def gen_graph(results_list, time):
    #tato fce generuje graf z jednoho záznamu
    results_list = list(map(float, results_list)) # radši převeď graf na floaty, může se stát že jsou to stringy
    avg = get_avg(results_list)
    global canvas
    num_of_rounds = [i for i in range(1, len(results_list) + 1)] # abych mohla udělat graf musím očíslovat kola

    # používám try except, aby když se něco pokazí nevypnul se celý program
    try:
        plt.close('all') # vymaž všechny minulé grafy abychom neplýtvali pamětí
        fig, ax = plt.subplots()
        colors = ['green' if result <= avg else 'blue' for result in results_list] # pokud je r.d. kratší než průměr tak je zelená jinak modrá

        # toto je nastavení grafu
        bars = ax.bar(num_of_rounds, results_list, color=colors) # co je sloupec (pořadí na reakční době)
        ax.bar_label(bars, padding=2) # ukaž hodnoty sloupců nad grafem
        ax.margins(0.07) # aby se hodnoty nad sloupcy nedotýkaly okraje
        ax.set_xticks(num_of_rounds) # osa x
        ax.set_xticklabels([str(num) for num in num_of_rounds]) # označení sloupců na ose x
        ax.set_title(f'Reakční doba při jednotlivých měřeních z {time}', pad=10) # název grafu
        ax.set_xlabel('pořadí') # název osy x
        ax.set_ylabel('reakční doba v milisekundách') # název osy y
        ax.grid(axis='y', linestyle='--', alpha=0.5) # udělá linky v grafu aby byl přehlednější

        # pokud existuje jiný graf tak ho smaž
        if canvas:
            canvas.get_tk_widget().destroy()

        # nakresli nový graf
        new_canvas = FigureCanvasTkAgg(fig, master=root)
        new_canvas.draw()
        new_canvas.get_tk_widget().grid(column=3, row=0, sticky='nsew')
        globals()['canvas'] = new_canvas

    except Exception as e:
        # pokud se něco pokazilo tak zobraz chybu
        errors_text.config(text=f"Při generování grafu se něco pokazilo: {e}")

def round(serial_inst):
    # toto je hlavní funkce, musí to být takto, aby to bylo spustitelné na tlačítko
    serial_inst.write(b'start') # řekni arduino že má začít měřit

    storage_file_results = RESULTS_STRG_PATH # path k textovému souboru k ukládání dat
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
                
                list_old_results() # aktualizuj list záznamů
                all_time_avg_text.config(text=f"{messages[3]}{get_all_time_avg(RESULTS_STRG_PATH)}")

                end = True # ukonči loop

            elif decoded_packet.startswith(">"):
                pass      
            else: # zaznamenej vysledek do listu (round results list)
                round_results_list.append(decoded_packet.replace("\r\n", ""))

    # vygeneruj graf            
    gen_graph(round_results_list, time)

def start_round(serial_inst):
    # tahle fce je potřeba, aby se zobrazila zpráva o tom že arduino testuje
    main_text.config(text=messages[1]) # oznam na obrazovce že arduino měří
    root.after(10, lambda: round(serial_inst)) # za chvilinku spusť hlavní fci

def list_old_results():
    # v listu na obrazovce se objeví data všeh záznamů uložených v souboru
    list_box.delete(0, tk.END)
    with open(RESULTS_STRG_PATH, "r") as f:
        results = f.readlines()
        f.close()
    for line in results:
        # do listu dej jednotlivá data záznamů
        if results.index(line) % 2 == 0:
            list_box.insert(tk.END, line.strip())

def load_selected(event):
    # když z listu něco vybereš načti to do podoby grafu
    selection = list_box.curselection()
    if selection:
        selected_index = selection[0]
        time = list_box.get(selected_index)
        with open(RESULTS_STRG_PATH, "r") as f:
            results = f.readlines()
            f.close()
        results_list = get_list_from_line(results[(selected_index * 2) + 1]) # vezmi záznam pod datem
        gen_graph(results_list, time) # vygeneruj z toho graf
        main_text.config(text=f"{messages[2]}{get_avg(results_list)}") # aktualizuj reakční dobu na aktuální záznam
        
# nastavení tkinteru (GUI)
def_font = (12)
root = tk.Tk()
root.title("Tester reakční doby")
frame = tk.Frame(root)
frame.grid(sticky="ns")
canvas = None

# nastavení textových polí
main_text = tk.Label(frame, text=messages[0], font=def_font, pady=15) # textové pole
all_time_avg_text = tk.Message(frame, text=f"{messages[3]}{get_all_time_avg(RESULTS_STRG_PATH)}", font=def_font, anchor="w", width=200) # zobrazí průměr napříč všemi záznamy
errors_text = tk.Label(frame, text="", font=(10), pady=10) # textové pole pro zobrazení případných chyb
list_label = tk.Label(frame, text="Historie záznamů", font=def_font, pady=15, padx=10)

all_time_avg_text.grid(column=2, row=1, pady=(10, 0))
main_text.grid(column=2, row=0, padx=(5, 10))
errors_text.grid(column=2, row=2, padx=(5, 10))
list_label.grid(column=0, row=0, padx=(15, 5))

# list kde se zobrazí kliknutelné minulé záznamy
list_box = tk.Listbox(frame, selectmode='single', height=23, width=23)
list_box.grid(column=0, row=1, sticky="ns", padx=(10, 5), pady=(0, 10), rowspan=2)
list_box.bind("<<ListboxSelect>>", load_selected)

# scrollbar k listu
listbox_scrollbar = tk.Scrollbar(frame, orient="vertical", command=list_box.yview)
list_box.configure(yscrollcommand=listbox_scrollbar.set)
listbox_scrollbar.grid(column=1, row=1, sticky="ns", pady=10, rowspan=2)

# tlačítko
start_button = tk.Button(frame, text="Start", command=lambda: start_round(serial_inst), font=def_font) # tlačítko start
start_button.grid(column=2, row=2)

list_old_results() # aktualizuj list záznamů na začátku
tk.mainloop() # spusť aplikaci
