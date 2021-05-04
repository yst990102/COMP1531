import jwt

SECRET = 'sempai'

# Login, Register
encoded_jwt = jwt.encode({'username': 'hunter'}, SECRET, algorithm='HS256')

# Every other route
print(jwt.decode(encoded_jwt, SECRET, algorithms=['HS256']))