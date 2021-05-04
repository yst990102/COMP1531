import sys

LOOP_MIN = 10
LOOP_MAX = 20

if len(sys.argv) != 2:
	sys.exit(1)

num = int(sys.argv[1])

if num not in [2, 3]:
	sys.exit(1)

for i in range(LOOP_MIN, LOOP_MAX):
	print(f"{i} ** {num} = {i ** num}")