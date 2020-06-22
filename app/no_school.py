from datetime import date
from datetime import timedelta

def all_sunday(year):
    d = date(year, 1, 1)                    # January 1st
    sunday = [d]
    d += timedelta(days = 6 - d.weekday())  # First Sunday
    sunday.append(d)
    while d.year == year:
       d += timedelta(days = 7)
       sunday.append(d)
    return sunday

def summerbreak(year):
    s_day = date(year,12,12)    # start of the summer holiday 
    e_day = date(year+1,1,6)     # end of the summer holiday
    sb_day = [s_day]
    eday =  s_day      
    for day in range((e_day - s_day).days):
       eday += timedelta(days = 1) 
       sb_day.append(eday)
    return sb_day
     
def push_to_monday(date):
    if date.weekday() == 5:
        return date + timedelta(days=2)
    if date.weekday() == 6:
        return date + timedelta(days=1)
    return date

def push_consecutive_to_monday(date):
    date2 = date + timedelta(days=1)
    if date.weekday() == 5 or date.weekday() == 6:
        date += timedelta(days=2)
    if date2.weekday() == 5 or date2.weekday() == 6:
        date2 += timedelta(days=2)
    return date, date2

def calculate_easter_sunday(year):
    a = year % 19
    b = year / 100
    c = year % 100
    d = b / 4
    e = b % 4
    f = (b + 8) / 25
    g = (b - f + 1) / 3
    h = (19 * a + b - d - g + 15) % 30
    i = c / 4
    k = c % 4
    L = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * L) / 451

    month = int((h + L - 7 * m + 114) / 31)
    day = int(((h + L - 7 * m + 114) % 31) + 1)
    return date(year, month, day)

def calculate_holidays(year):
    holidays = []

    #monday = 0, sunday = 6
    
    newyears1, newyears2 = push_consecutive_to_monday(date(year, 1, 1))
    holidays.append(newyears1)
    holidays.append(newyears2)
    #print (holidays)

    waitangiday = push_to_monday(date(year, 2, 6))
    holidays.append(waitangiday)
    #print (holidays)

    # The school not open on Ester Tuesday 
    eastersunday = calculate_easter_sunday(year)
    goodfriday = eastersunday - timedelta(days=2)
    eastermonday = eastersunday + timedelta(days=1)
    eastertuesday = eastersunday + timedelta(days=2)
    holidays.append(goodfriday)
    holidays.append(eastermonday)
    holidays.append(eastertuesday)


    anzacday = push_to_monday(date(year, 4, 25))
    holidays.append(anzacday)
	
    # queens birthday, first monday in june
    queensbirthday = date(year, 6, 1)
    if queensbirthday.weekday() == 6:
        queensbirthday += timedelta(days=1)
    elif queensbirthday.weekday() != 0:
        queensbirthday += timedelta(days=7 - queensbirthday.weekday())
    holidays.append(queensbirthday)

    # labour day, 4th monday in october
    labourday = date(year, 10, 1)
    while labourday.weekday() != 0:
        labourday += timedelta(days=1)
    labourday += timedelta(weeks=3)
    holidays.append(labourday)

    # show day, second friday after the first tuesday in november
    showday = date(year, 11, 1)
    while showday.weekday() != 1:
        showday += timedelta(days=1)
    showday += timedelta(days=10)
    holidays.append(showday)

    xmasday, boxingday = push_consecutive_to_monday(date(year, 12, 25))
    holidays.append(xmasday)
    holidays.append(boxingday)

    return holidays

def noschool_day(year):
    sundays = all_sunday(year)
    summerdays = summerbreak(year)
    p_days = calculate_holidays(year)
    merge = sorted(list(set(sundays+ summerdays+  p_days)))
    return merge



