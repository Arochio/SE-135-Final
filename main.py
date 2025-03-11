#Notes:
#If program doesn't run, try these commands in the terminal first
#pip3 install pandas --upgrade
#pip3 install matplotlib --upgrade
#pip3 install openpyxl --upgrade

# All the Imports that we need :3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy
import datetime
from statistics import mean

#Constants
MODEL_INDEX = 0
DATE_INDEX = 2
PRICE_INDEX = 8

# Reading the file
table = pd.read_excel('SeedUnofficialAppleData.xlsx', skiprows=1)
dataIndex = 0
indexList = []
col0 = table.iloc[:,0]
finalData = []

# scatter function
def scatterPlot(data, _label):

    fig, ax = plt.subplots(figsize=(10,6))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.scatter(date, data, label=_label)

    formatter = ticker.StrMethodFormatter('${x:,.2f}')
    ax.yaxis.set_major_formatter(formatter)

    plt.legend(loc="best")

    ax.set_title("Cost of iPhones over time")
    ax.set_ylabel("Cost")
    ax.set_xlabel("Release Date")

    plt.gcf().autofmt_xdate()
    plt.savefig(_label + ".png")

# Fill in all null values
col0 = col0.fillna("")

#Create list of index values of where new phone models live
for i in range(0, len(col0)):
    if col0[i] != "":
        indexList.append(i)
indexList.append(len(col0))


#Removing nulls and replacing weird tabs with spaces
#Also squished multirow datasets into one row where applicable
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

#important columns of finalData for quick access
model = finalData[MODEL_INDEX].copy()
date = finalData[DATE_INDEX].copy()
price = finalData[PRICE_INDEX].copy()

# find the indexes of phones with multiple model types (ex. max/mini versions)
iModel = []
for i in range(0,len(model)):
    if "/" in model[i]:
        iModel.append(i)

#seperate the multi model phones into individual entries
for i in reversed(iModel):
        if "Max:" in price[i]:
            price += price.pop(i).split("Max:",1)
        elif "Mini:" in price[i]:
            price += price.pop(i).split("Mini:",1)
        elif "Plus:" in price[i]:
            price += price.pop(i).split("Plus:",1)
        if "/" in model[i]:
            model += model.pop(i).split('/')
        if "/" in date[i]:
            date += date.pop(i).split('/')
        else:
            tempDate = date.pop(i)
            date.append(tempDate)
            date.append(tempDate)

#Do the same as above but for price
tempPrice = []
for i, data in enumerate(price):
    if "*" in data:
        tempPrice += data.split("*")

while "" in tempPrice:
    tempPrice.remove("")
price = tempPrice

median = []
min = []
max = []

#Strip unneeded strings and then calculate median, minimum, and maximum for each phone model
for i, data in enumerate(price):
    price[i] = data.replace(" ", "").replace("$", "").replace("Plus:", "")
    tempVar = price[i].split("/")
    tempVar = list(map(int, tempVar))
    median.append(numpy.median(tempVar))
    min.append(numpy.min(tempVar))
    max.append(numpy.max(tempVar))

#Convert release date into DateTime values
for i, data in enumerate(date):
    if "(" in date[i]:
        date[i] = date[i][:data.find("(")] + data[data.find(")") + 1:]
        date[i] = date[i].strip()
    date[i] = date[i].replace(",", "")
    format = '%B %d %Y'
    date[i] = datetime.datetime.strptime(date[i], format)

#Retrieve all x and y values for use in best fit line calculations
allXvalues =[]
allYvalues = []
for i in range(0,len(median)):
    allYvalues.append(int(min[i]))
    allYvalues.append(int(max[i]))
    allYvalues.append(int(median[i]))
    #need 3 copies of date values in order to compensate for increased 
    allXvalues.append(int(date[i].timestamp())/86400)
    allXvalues.append(int(date[i].timestamp())/86400)
    allXvalues.append(int(date[i].timestamp())/86400)

#Make the lists into numpy arrays so that we can use them better
npX = numpy.array(allXvalues)
npY = numpy.array(allYvalues)

#y = mx + b calcs 
bfSlope = (((mean(npX)*mean(npY)) - mean(npX*npY)) / ((mean(npX)*mean(npX)) - mean(npX*npX)))
bfIntercept = mean(npY) - bfSlope*mean(npX)
regression_line = [(bfSlope*x)+bfIntercept for x in npX]

#Plotting
fig, ax = plt.subplots(figsize=(10,6))

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())

plt.scatter(date, median, label='Median')
plt.scatter(date, min, c="#FF0000", label='Min')
plt.scatter(date, max, c="#00FF00", label='Max')
plt.plot(npX, regression_line)

formatter = ticker.StrMethodFormatter('${x:,.2f}')
ax.yaxis.set_major_formatter(formatter)
plt.legend(loc="best")
ax.set_title("Cost of iPhones over time")
ax.set_ylabel("Cost")
ax.set_xlabel("Release Date")
plt.gcf().autofmt_xdate()
plt.savefig("Combined.png")

scatterPlot(median, "Medians")
scatterPlot(min, "Min")
scatterPlot(max, "Max")