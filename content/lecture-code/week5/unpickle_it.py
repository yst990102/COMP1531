# https://wiki.python.org/moin/UsingPickle

import pickle

DATA = pickle.load(open("export.p", "rb")) # alternative way
print(DATA)
