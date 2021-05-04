import sys

argc = len(sys.argv)

empty = True
if argc > 0:
    empty = False

if not empty:
    if argc == 2:
        print("Nearly there")
    elif argc == 3:
        if sys.argv[1] == "H" and sys.argv[2] == "I":
            print("HI to you too")
        else:
             pass
else:
  print("Please enter two letters as command line")
