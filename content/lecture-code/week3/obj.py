from datetime import date

today = date(2019, 9, 26)

# 'date' is its own type
print(type(today))

# Attributes of 'today'
print(today.year)
print(today.month)
print(today.day)

# Methods of 'today'
print(today.weekday())
print(today.ctime())