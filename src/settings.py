import serial

RESULTS_STRG_PATH = "src/results_new.txt" 
SERIAL_PORT = "COM6" # pokud neodpovídá port, je potřeba ho nastavit

def get_port_list():
    # jaký je správný se zjistí díky této fci
    ports = serial.tools.list_ports.comports()
    list_of_ports = []

    for port in ports:
        list_of_ports.append(str(port))
    return list_of_ports

# print stačí odkomentovat a spustit tenhle soubor, pak port přepsat
#print(get_port_list)