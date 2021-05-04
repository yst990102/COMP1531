import jwt

SECRET = 'applepineappleorange'

encoded_jwt = jwt.encode({'some': 'payload'}, SECRET, algorithm='HS256')
print(jwt.decode(encoded_jwt, SECRET, algorithms=['HS256']))