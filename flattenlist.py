test = [[1,2,[3]],4]

def flatten(nestlist):
    for i in nestlist:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i

print(list(flatten(test)))