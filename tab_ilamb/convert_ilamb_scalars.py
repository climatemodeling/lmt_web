#!/usr/bin/env python


import json, collections
from bs4 import BeautifulSoup
import sys



def read_jsontree(models, parentObj, parentScore):

    parentList = []
    parentDict = {}
    for m in parentObj.keys():

        if "Score" not in m and m != "children":
           parentDict['metric'] = m


        childObj = parentObj[m]


        for key in childObj.keys():

            if parentScore != "None" and key == parentScore:
               parentDict['scoreboard'] = key
               for n, mod in enumerate(models):
                   parentDict[str(mod)] = childObj[key][n]

               if "children" in childObj.keys() and childObj["children"] != {}:
                  parentDict["_children"] = []
                  parentDict["_children"] = read_jsontree(models, childObj["children"], key)
               parentList.append(parentDict.copy())

            if parentScore == "None" and key != "children":
               parentDict['scoreboard'] = key

               for n, mod in enumerate(models):
                   parentDict[str(mod)] = childObj[key][n]

               if "children" in childObj.keys() and childObj["children"] != {}:
                  parentDict["_children"] = []
                  parentDict["_children"] = read_jsontree(models, childObj["children"], key)

               parentList.append(parentDict.copy())

    return parentList
        
                   

with open("ilamb_index.html") as fp:
    soup = BeautifulSoup(fp, features="lxml")

for se in soup.find_all('select'):

    if se.get_attribute_list("id")[0] == "RegionOption":
       regStrs = se.get_text()
    if se.get_attribute_list("id")[0] == "ScalarOption":
       scaStrs = se.get_text()


modList=[]
for hd in soup.find_all("th"):

   if hd.get_text() != '':
      modList.append(hd.get_text())

regList = regStrs.strip().split("\n")
scaList = scaStrs.strip().split("\n")




#models=["BCC-CSM2-MR", "BCC-ESM1", "CAMS-CSM1-0", "CESM2", "CESM2-WACCM", "EC-Earth3-Veg", "FGOALS-f3-L", 
#"GFDL-AM4", "GFDL-CM4", "GISS-E2-1-G", "IPSL-CM6A-LR", "MIROC6", "MRI-ESM2-0", "SAM0-UNICON"]

models = modList

# test a new code





metricList=[]
with open("scalars.json", "r") as jn:
    vars=json.load(jn, object_pairs_hook=collections.OrderedDict) 

    metricList = read_jsontree(models, vars, "None")

with open ("my.json", "w") as fw:
     json.dump(metricList, fw)

sys.exit()

metricList=[]
with open("scalars.json", "r") as jn:
    vars=json.load(jn, object_pairs_hook=collections.OrderedDict) 

    for topmetric in vars.keys():


        metricDict={}
        metricDict['metric'] = topmetric

        #print("1st", topmetric)
        print(vars[topmetric].keys())

        continue
        for score in vars[topmetric].keys():
            if score != 'children':    # different score board
               metricDict['scoreboard'] = score
               for n, mod in enumerate(models):
                   metricDict[mod] = vars[topmetric][score][n]

               metricDict['_children']=[]
               for sndmetric in vars[topmetric]['children'].keys():

                   sndDict={}
                   sndDict['metric'] = sndmetric

                   #print ("2nd", sndmetric)
                   #print (vars[topmetric]['children'][sndmetric].keys())

                   #print (topmetric, sndmetric, score)
                   for m, mod in enumerate(models):
                       if score in vars[topmetric]['children'][sndmetric].keys():
                          sndDict[mod] = vars[topmetric]['children'][sndmetric][score][m]
                       else:
                          sndDict[mod] = -999.

                   sndDict['_children']=[]
                   for thdmetric in vars[topmetric]['children'][sndmetric]['children'].keys():
                       thdDict={}
                       thdDict['metric']=thdmetric
                              #print ("3rd", thdmetric)
                              #print (vars[topmetric]['children'][sndmetric]['children'][thdmetric].keys())

                                     #-print (thdmetric, gdscore)

                       #print (thdmetric, score, vars[topmetric]['children'][sndmetric]['children'][thdmetric].keys())

                       for k, mod in enumerate(models):
                           if score in vars[topmetric]['children'][sndmetric]['children'][thdmetric].keys():
                              thdDict[mod] = vars[topmetric]['children'][sndmetric]['children'][thdmetric][score][k]
                           else:
                              thdDict[mod] = -999.

                       sndDict['_children'].append(thdDict)
                   metricDict['_children'].append(sndDict)
               #print(metricDict['scoreboard'])
               metricList.append(metricDict.copy())


for me in metricList:
    print (me['scoreboard'])

with open ("my.json", "w") as fw:
     json.dump(metricList, fw)

