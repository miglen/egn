# -*- coding: utf-8 -*-
import sys
import random


def generate(**kwargs):
    '''
    Method to generate numbers.
    '''

    if 'year' in kwargs:
        year = int(kwargs['year'])
    else:
        year = random.randint(1800, 2099)

    if 'month' in kwargs:
        month = int(kwargs['month'])
    else:
        month = random.randint(1, 12)

    if 'day' in kwargs:
        day = int(kwargs['month'])
    else:
        day = random.randint(1, 31)

    if 'sex' in kwargs:
        sex = int(kwargs['sex'])
    else:
        sex = random.randint(1, 2)

    if 'limit' in kwargs:
        limit = int(kwargs['limit'])
    else:
        limit = random.randint(1, 2)

    if 'region' in kwargs:
        region = int(kwargs['region'])
    else:
        region = random.randint(1, 999)
    print(day, month, year, sex, region, limit)
    return '9941011142'


def validate(egn):
    '''
    Check Bulgarian EGN codes for validity
    full information about algoritm is available here
    http://www.grao.bg/esgraon.html#section2
    https://gist.github.com/vstoykov/1137057
    '''
    def check_valid_code(egn):
        egn_weights = (2, 4, 8, 5, 10, 9, 7, 3, 6)
        try:
            my_sum = sum([weight * int(digit) for weight,
                         digit in zip(egn_weights, egn)])
            return int(egn[-1]) == my_sum % 11 % 10
        except ValueError:
            return False

    def check_valid_date(egn):
        from datetime import datetime
        try:
            year, month, day = int(egn[0:2]), int(egn[2:4]), int(egn[4:6])
        except:
            return False
        if month >= 40:
            month -= 40
            year += 2000
        elif month >= 20:
            month -= 20
            year += 1800
        else:
            year += 1900
        try:
            # Gregorian calendar adoption: 31/03/1916 > +13 days > 14/04/1916
            if year == 1916 and month == 4 and day <= 13:
                return False

            datetime.strptime('%s-%s-%s' % (year, month, day), "%Y-%m-%d")
            return True

        except ValueError:
            return False

    if isinstance(egn, int):
        egn = str('{0:0=10d}'.format(egn))

    return len(egn) == 10 and check_valid_code(egn) and check_valid_date(egn)


def main():
    """Entry point for the application script"""
    if len(sys.argv) <= 1:
        print("This is a help message")
        exit()
    if validate(sys.argv[1]):
        print("{} is valid!".format(sys.argv[1]))
        exit()
    else:
        print("{} is invalid!".format(sys.argv[1]))
        exit(1)
