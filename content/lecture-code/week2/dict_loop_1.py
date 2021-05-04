userData = [
    {
        'name' : 'Sally',
        'age' : 18,
        'height' : '186cm',
    },
    {
        'name' : 'Bob',
        'age' : 17,
        'height' : '188cm',
    },
]

for user in userData:
    print("Whole user: ", user)
    for part in user:
        print(f"  {part}")
