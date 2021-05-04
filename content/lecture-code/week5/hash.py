import hashlib
#print("mypassword")
#print("mypassword".encode())
#print(hashlib.sha256("mypassword".encode()))
print(hashlib.sha256("passwordpassword".encode()).hexdigest())


# (Number of possible characters) ^ Length of the password
# passwordpassword