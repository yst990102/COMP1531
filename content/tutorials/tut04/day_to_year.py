from calendar import isleap

origin_year = 1970

def day_to_year(days):
    year = origin_year

    while days > 365:
        if isleap(year):
            if days > 366:
                days -= 366
                year += 1
        else:
            days -= 365
            year += 1

    return year
