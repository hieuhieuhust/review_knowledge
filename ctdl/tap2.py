def anagrams(list): 
    dictt = {}
    for i in range(len(list)):
        nhan= "".join(sorted(list[i]))
        if nhan not in dictt:
            dictt[nhan] = [list[i]]
        else:
            dictt[nhan].append(list[i])
    return list(dictt.values())
        
           

        
        
        
        
        