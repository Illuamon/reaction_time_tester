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
    round_results = round_results.replace("'", "").replace("[", "").replace("]", "").strip("\n")
    results_list = round_results.split(", ")
    #pocitani avg
    sum = 0
    for num in results_list:
        sum += num
    
    avg = sum / len(results_list)

    return (results_list, avg)

