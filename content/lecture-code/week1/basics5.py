x = 5
y = 6
point = (x, y)
print(point)

a, b = point # destructuring
print(f"{a}, {b}")

names = [ "Giraffe", "Llama", "Penguin" ]
for id, name in enumerate(names):
  print(f"{id} {name}")