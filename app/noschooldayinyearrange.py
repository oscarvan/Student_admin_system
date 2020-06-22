from app.no_school import noschool_day

'''year1 is the start year and year 2 is the end year
the code will produce a list of no school dates in the year range
the bottom code is to loop through the return list of dates'''

def no_school_years(year1,year2):
    no_school_day =[]
    for year in range(year1,year2+1):
        year = year
        no_school_day.append(noschool_day(year))
    return no_school_day

#no_school_years(2018,2019)


'''code to loop through a year range dates, as the list contains i(year range) sublists
    i= 0    
    while i < len(no_school_day):
        for day in no_school_day[i]:
            print (day.strftime("%Y-%m-%d"))
           # print(type(day.strftime("%Y-%m-%d")))
        i = i + 1
'''
