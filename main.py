#pip3 install pandas --upgrade
#pip3 install matplotlib --upgrade
#pip3 install openpyxl --upgrade

import pandas as pd
import matplotlib.pyplot as plt

MODEL_INDEX = 0
DATE_INDEX = 2
PRICE_INDEX = 8

table = pd.read_excel('SeedUnofficialAppleData.xlsx', skiprows=1)
dataIndex = 0
indexList = []
col0 = table.iloc[:,0]
finalData = []

col0 = col0.fillna("")

for i in range(0, len(col0)):
    if col0[i] != "":
        indexList.append(i)
indexList.append(len(col0) - 1)

for i in range(0, len(table.columns)):
    tempStr = ""
    tempList = []
    col = table.iloc[:, i]
    col = col.fillna("")
    for j in range(1, len(indexList)):
        for k in range(indexList[j - 1],indexList[j]):
            tempStr += str(col[k]) + " "
        tempList.append(tempStr.replace('\xa0', " ").strip())
        tempStr = ""
    
    finalData.append(tempList)

model = finalData[MODEL_INDEX]
date = finalData[DATE_INDEX]
price = finalData[PRICE_INDEX]
print(model)
print()
print(date)
print()
print(price)
print()