from evaluation_utils import *

ma1_dict_compare_n100 = {}
ma2_dict_compare_n100 = {}
ma3_dict_compare_n100 = {}

for i,ma_topologies in enumerate([ma1_topologies,ma2_topologies,ma3_topologies]):
    i = i+1
    if (i==1) or (i==2):
        continue
    
    for topology in ma_topologies:
        l = os.listdir(topology)
        
        maxDeliveryTime = {}
        avgDeliveryTime = {}
        avgDeliveryNodes = {}
        totalMsgSent = {}
        
        for file in l:
            top = "_n"+str(topology).split("/n")[1]+"_"+str(file)
            n, k, t, d = extract_info(top)
            if t not in avgDeliveryNodes:
                avgDeliveryNodes[t] = {}
            if t not in avgDeliveryTime:
                avgDeliveryTime[t] = {}
            if t not in maxDeliveryTime:
                maxDeliveryTime[t] = {}
            if t not in totalMsgSent:
                totalMsgSent[t] = {}
                
            avgDeliveryNodes[t][d] = []
            avgDeliveryTime[t][d] = []
            maxDeliveryTime[t][d] = []
            totalMsgSent[t][d] = []
            with open(topology/file,"r") as f:
                data = json.load(f)
                for test in data["tests"]:
                    avgDeliveryNodes[t][d].append(data["tests"][test]["avgDeliveryNodes"])
                    avgDeliveryTime[t][d].append(data["tests"][test]["avgDeliveryTime"])
                    maxDeliveryTime[t][d].append(data["tests"][test]["maxDeliveryTime"])
                    totalMsgSent[t][d].append(data["tests"][test]["totalMsgSent"])
        
        dict_all = {}
        dict_all["avgDelTime"] = avgDeliveryTime
        dict_all["avgDelNodes"] = avgDeliveryNodes
        dict_all["maxDelTime"] = maxDeliveryTime
        dict_all["totMsgSent"] = totalMsgSent
        
        if (i == 1):
            dict_top = ma1_topologies
            dict_compare_n100 = ma1_dict_compare_n100
        if (i == 2):
            dict_top = ma2_topologies
            dict_compare_n100 = ma2_dict_compare_n100
        if (i == 3):
            dict_top = ma3_topologies
            dict_compare_n100 = ma3_dict_compare_n100
            
        if (("_n100_k6" in dict_top[topology] ) or ("_n99_k6" in dict_top[topology])):
            dict_compare_n100[dict_top[topology]] = {}
            dict_compare_n100[dict_top[topology]]["avgDelTime"] = avgDeliveryTime
            dict_compare_n100[dict_top[topology]]["avgDelNodes"] = avgDeliveryNodes
            dict_compare_n100[dict_top[topology]]["maxDelTime"] = maxDeliveryTime
            dict_compare_n100[dict_top[topology]]["totMsgSent"] = totalMsgSent

#print(ma3_dict_compare_n100["multi_wheel_n99_k6"])

plot_graph_compare_slim(ma3_dict_compare_n100, ma3_topologies, 4, 100, 6, f"compare_topologies_n100_k6_t5.jpg")
    
    
    
    