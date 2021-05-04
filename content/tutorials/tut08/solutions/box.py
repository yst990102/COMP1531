import sys

WIDTH = 10 # DRY
HEIGHT = 10 # DRY

def border(i, j): # Top-down thinking
    return i == 0 or i == WIDTH - 1 or j == 0 or j == HEIGHT - 1

if __name__ == '__main__':
    for rows in range(HEIGHT): # KISS
        for cols in range(WIDTH): # KISS
            if border(cols, rows):
                sys.stdout.write('*')
            else:
                sys.stdout.write(' ')
        sys.stdout.write("\n")