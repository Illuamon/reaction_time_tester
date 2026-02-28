def get_list_from_line(line):
    #vyuzivam casto, prevede linku v textovem souboru do listu floatů
    results_list = line.replace("'", "").replace("[", "").replace("]", "").strip("\n").split(", ")
    return list(map(float, results_list))

def get_avg(lst):
    #nechci full float proto zaokrouhluju
    lst = list(map(float, lst))
    sum = 0
    for num in lst:
        sum += num
    avg = sum / len(lst)
    return round(avg, 2)

def get_round_result_and_avg(round_no, path_result_storage):
    #hodí se pro starší záznamy
    #return tuple (list vysledku, prumer)
    line_to_access = round_no * 2 
    with open(path_result_storage, "r") as f:
        round_results = f.readlines() 
        if len(round_results) < line_to_access:
            raise Exception("řádek v souboru není")
        round_results = round_results[line_to_access - 1]
        f.close()

    results_list = get_list_from_line(round_results)
    avg = get_avg(results_list)

    return (results_list, avg)

def get_all_time_avg(path_result_storage):
    #returne average vsech zaznamu ve file
    with open(path_result_storage, "r") as f:
        file_content = f.readlines() 
        f.close()
    
    results = []
    for line in file_content:
        if line.startswith("["):
            line = get_list_from_line(line)
            results.extend(line)
    
    return get_avg(results)

