test = "October 23, 2020 (12 Pro) / November 13, 2020 (12 Pro Max)"
listTest = ["iOS", "(", ")", "iPhone", "OS", " ", "Pro", "Max", "Mini"]
mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug" "Sep", "October", "Nov", "Dec"]
#for i in listTest:
#    test = test.replace(i, "")
#test = test.split("/")
i = 2007
index = ""
index2 = ""
while True:
    if test.find(str(i)) != -1:
        index = test.find(str(i)) + 5
    i += 1
    
    if i > 2025:
        break
for j in mon:
    if test.find(j) != -1:
        index2 = test.find(j)

print(index2)
print(index)
print(test[index2:index])