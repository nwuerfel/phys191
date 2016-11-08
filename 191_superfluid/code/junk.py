def subtract_addendum(addendum_data,num):

    hcap = addendum_data[1]
    temp = addendum_data[0]
    
    print hcap
    print temp
    
    maxi_list = []
    mini_list = []
    
    for i in temp:
        if i >= num:
            maxi_list.append(i)
        else:
            mini_list.append(i)
   
    temp_max = min(maxi_list)
    temp_min = max(mini_list)
  
    temp_list = list(temp)
 
    hcap_max = hcap[temp_list.index(temp_max)]
    hcap_min = hcap[temp_list.index(temp_min)]
    
    slope = (hcap_max - hcap_min) / (temp_max - temp_min)
    
    return hcap_min + slope * (num - temp_min)


