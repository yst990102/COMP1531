'''
TODO Complete this file by following the instructions in the lab exercise.
'''

integers = [1, 2, 3, 4, 5]
# add the number 6 to the list (using the append function)
integers.append(6)

# add all of the numbers up using a for loop
result = 0
for i in integers:
    result += i
# print out the result
print(result)


# At the bottom of the file add the line "print(sum(integers))"
print(sum(integers))