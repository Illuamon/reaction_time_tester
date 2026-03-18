# v tomto souboru jsou pomocné fce hlavně k práci s souborem se záznamy dat

def get_list_from_line(line):
    # převede linku z textového souboru do validního listu pro ostatní fce
    results_list = line.replace("'", "").replace("[", "").replace("]", "").strip("\n").split(", ")
    return list(map(float, results_list))

def get_avg(lst):
    #nechci full float proto zaokrouhluju
    lst = list(map(float, lst)) #ujistit se, že je input správný, převedeme ho na list floatů
    sum = 0
    for num in lst:
        sum += num
    avg = sum / len(lst)
    return round(avg, 2)

def get_all_time_avg(path_result_storage):
    #returne average vsech zaznamu v souboru
    with open(path_result_storage, "r") as f:
        file_content = f.readlines() 
        f.close()
    
    results = []
    for line in file_content:
        if line.startswith("["):
            line = get_list_from_line(line)
            results.extend(line)
    
    return get_avg(results)


