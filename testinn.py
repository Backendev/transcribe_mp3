from pickle import FALSE


results = {}
j = 0
times = [0, 674, 1027, 1723, 1940, 2250, 2977, 3143, 3453, 3642, 3878, 4013, 4661, 4880, 5105, 6505, 7086, 7319, 7477, 7786, 8523, 8758, 8920, 9327]
hallazgo = {'0': ['India'], '674': ['bus 28', 'West 28th', 'has 28', '28'], '1940': ['visits capital', 'with its capital', 'read its capital', 'did its capital', 'visits Capitol'], '4661': ['New Delhi', 'at New Delhi', 'New Deli'], '6505': ['just looking', 'richest looking', 'which is looking', "witch's looking", 'Duchess looking'], '7319': ['in the North'], '8523': []}
lista = ['India', 'has', '28', 'states', 'with', 'its', 'capital', 'New', 'Delhi', 'which', 'is', 'located', 'in', 'the', 'north', 'of', 'India']


i_times = 0
i_hallazgo = 0
i_list =0
results = {}
reco = True
ha = False
j = 0
ha_ant = 0
i = 0
l_times = list(hallazgo.keys())
largo = 0
hal=False
temp_k = lista
actual = 0
dif = 0
for i in times:
    print(i)
    actual += 1
    init = 0
    ha = False
    if str(i) in hallazgo.keys():
        for k in hallazgo[str(i)]:
            list_sp = k.split()
            lon_list = len(list_sp)
            time = str(i)
            for ij in range(init,len(temp_k)):
                l_bus = temp_k[ij:ij+lon_list]
                bus = " ".join(l_bus)
                if k.lower() == bus.lower():
                    print(f"temp - {temp_k[ij:ij+lon_list]} time{i}")
                    temp_k = temp_k[ij+lon_list::]
                    ha = True
                    print(str(i))
                    print("Si")
                    
                    dif = dif + (ij + lon_list)
                    item = dif - lon_list
                    item_l = item + (lon_list)
                    if item_l == item:
                        results[item] = actual -1
                    else:
                        for items in range(item,item_l):
                            print(items)
                            results[items] = actual -1
                    print(f"Item {item} dif {item + (lon_list-1)}")
                    
                    print(f"Item  {lista[item]} hasta {lista[item + (lon_list -1 )]}")
                    break
            if ha:
                print("www")
                print(temp_k)
                
                break
            print()
result_fin = {}
ant = 0
print(results)
for it in range(0,len(lista)):
    if it in results.keys():
        result_fin[it] = {lista[it]:times[results[it]]}
        ant = results[it]
    else:
        result_fin[it] = {lista[it]:times[ant + 1]}
print(result_fin)
