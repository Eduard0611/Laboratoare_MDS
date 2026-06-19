def chunk(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def flatten(lst_of_lsts):
    return [item for sublist in lst_of_lsts for item in sublist]