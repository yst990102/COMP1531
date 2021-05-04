import sys
from PIL import Image

if len(sys.argv) == 6:
    x1 = int(sys.argv[2])
    x2 = int(sys.argv[4])
    y1 = int(sys.argv[3])
    y2 = int(sys.argv[5])
    imageObject = Image.open(sys.argv[1])
    cropped = imageObject.crop((x1, y1, x2, y2))
    cropped.save(sys.argv[1])

