test = "aflkjsdfljsdflkj 2.3.4..3.2.0 asldkjflasdkjfl;skdj"
test2 = test.split()
print(test2)

low = test.index(".")
high = low
loop1 = True
loop2 = True

while loop1 or loop2:
    if test[low - 1] != " ":
        low -= 1
    else:
        loop1 = False
    if test[high + 1] != " ":
        high += 1
    else:
        loop2 = False

test2 = test[low:high + 1]
print(test2)