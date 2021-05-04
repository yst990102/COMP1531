import sys

for line in sys.stdin:
    hour = int(line[:2])
    minute = int(line[2:4])
    
    pm = hour >= 12
    if pm and hour != 12:
        hour -= 12
        
    pad_hour = hour < 10
    pad_minute = minute < 10

    result = ''
    if pad_hour:
        result += '0'
    result += str(hour)
    
    result += ':'
    
    if pad_minute:
        result += '0'
    result += str(minute)
    
    if pm:
        result += ' PM'
    else:
        result += ' AM'
        
    print(result)
