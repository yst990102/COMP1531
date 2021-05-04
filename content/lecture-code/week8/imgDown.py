import urllib.request
import sys

if len(sys.argv) == 3:
    urllib.request.urlretrieve(sys.argv[1], sys.argv[2])
