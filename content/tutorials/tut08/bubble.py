import sys

if __name__ == '__main__':
    lst = []
    for i in range(1, len(sys.argv)):
        lst.append(int(sys.argv[i]))
    doneSorting = False
    while not doneSorting:
        doneSorting = True
        for i in range(len(sys.argv) - 2):
            if lst[i] > lst[i + 1]:
                tmp = lst[i]
                lst[i] = lst[i + 1]
                lst[i + 1] = tmp
                doneSorting = False

    print(lst)