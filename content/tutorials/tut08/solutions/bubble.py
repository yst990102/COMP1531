import sys

def swapNext(lst, i): # Top down
    tmp = lst[i]
    lst[i] = lst[i + 1]
    lst[i + 1] = tmp

def shouldSwapNext(lst, i): # Top down
    return lst[i] > lst[i + 1]

if __name__ == '__main__':
    lst = []
    size = len(sys.argv) # DRY
    for i in range(1, size):
        lst.append(int(sys.argv[i]))

    doneSorting = False
    while not doneSorting:
        doneSorting = True
        for i in range(size - 2):
            if shouldSwapNext(lst, i):
                swapNext(lst, i)
                doneSorting = False

    print(lst)

# or even better
"""
def makeInt(i):
    return int(i)

print(list(map(makeInt, sorted(sys.argv[1:]))))
"""