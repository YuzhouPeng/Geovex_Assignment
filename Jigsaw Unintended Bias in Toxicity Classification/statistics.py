import csv


with open('/Users/pengyuzhou/Downloads/train.csv', 'r') as f:
    next(f)
    reader = csv.reader(f)
    count = 0
    rows = [0,0,0,0,0,0,0,0,0]
    rows1 = [0,0,0,0,0,0,0,0,0]

    for row in reader:
        count+=1
    print("total = {}".format(count))
    f.seek(0)
    for row in reader:
        # print(row)
        for i in range(9):
            if row[8+i]!='':
                rows1[i]+=1
            if row[8+i]=='':
                rows[i]+=1
    print("empty values = {}".format(rows1))
    print("non empty values = {}".format(rows))