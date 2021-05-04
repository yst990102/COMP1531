import sys

import calmath

if len(sys.argv) != 3:
    print("Usage: importto.py month dayofmonth")
else:
    print(calmath.daysIntoYear(int(sys.argv[1]), \ 
                               int(sys.argv[2])))