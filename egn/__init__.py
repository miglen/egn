# -*- coding: utf-8 -*-
import argparse
import sys
import random

egn_regions = {
    43: {'bg': 'Благоевград', 'en': 'Blagoevgrad'},  # 000 - 043
    93: {'bg': 'Бургас', 'en': 'Burgas'},  # 044 - 093
    139: {'bg': 'Варна', 'en': 'Varna'},  # 094 - 139
    169: {'bg': 'Велико Търново', 'en': 'Veliko Turnovo'},  # 140 - 169
    183: {'bg': 'Видин', 'en': 'Vidin'},  # 170 - 183
    217: {'bg': 'Враца', 'en': 'Vratza'},  # 184 - 217
    233: {'bg': 'Габрово', 'en': 'Gabrovo'},  # 218 - 233
    281: {'bg': 'Кърджали', 'en': 'Kurdzhali'},  # 234 - 281
    301: {'bg': 'Кюстендил', 'en': 'Kyustendil'},  # 282 - 301
    319: {'bg': 'Ловеч', 'en': 'Lovech'},  # 302 - 319
    341: {'bg': 'Монтана', 'en': 'Montana'},  # 320 - 341
    377: {'bg': 'Пазарджик', 'en': 'Pazardzhik'},  # 342 - 377
    395: {'bg': 'Перник', 'en': 'Pernik'},  # 378 - 395
    435: {'bg': 'Плевен', 'en': 'Pleven'},  # 396 - 435
    501: {'bg': 'Пловдив', 'en': 'Plovdiv'},  # 436 - 501
    527: {'bg': 'Разград', 'en': 'Razgrad'},  # 502 - 527
    555: {'bg': 'Русе', 'en': 'Ruse'},  # 528 - 555
    575: {'bg': 'Силистра', 'en': 'Silistra'},  # 556 - 575
    601: {'bg': 'Сливен', 'en': 'Sliven'},  # 576 - 601
    623: {'bg': 'Смолян', 'en': 'Smolyan'},  # 602 - 623
    721: {'bg': 'София', 'en': 'Sofia'},  # 624 - 721
    751: {'bg': 'София (окръг)', 'en': 'Sofia (county)'},  # 722 - 751
    789: {'bg': 'Стара Загора', 'en': 'Stara Zagora'},  # 752 - 789
    821: {'bg': 'Добрич', 'en': 'Dobrich'},  # 790 - 821
    843: {'bg': 'Търговище', 'en': 'Targovishte'},  # 822 - 843
    871: {'bg': 'Хасково', 'en': 'Haskovo'},  # 844 - 871
    903: {'bg': 'Шумен', 'en': 'Shumen'},  # 872 - 903
    925: {'bg': 'Ямбол', 'en': 'Yambol'},  # 904 - 925
    999: {'bg': 'Друг', 'en': 'Other'}}  # 926 - 999


def generate(**kwargs):
    '''
    Method to generate numbers.
    '''

    return '9941011142'


def get_date(egn):
    '''
        Get the date information from the EGN
        Return hash with year, month, day and datetime.
    '''
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

        dt = datetime.strptime('%s-%s-%s' % (year, month, day), "%Y-%m-%d")
        return {'year': year, 'month': month, 'day': day, 'datetime': dt}

    except ValueError:
        return False


def validate(egn):
    '''
        Check Bulgarian EGN codes for validity
        full information about algoritm is available here
        http://www.grao.bg/esgraon.html#section2
        https://gist.github.com/vstoykov/1137057
    '''
    if isinstance(egn, int):
        egn = str('{0:0=10d}'.format(egn))

    def check_valid_code(egn):
        egn_weights = (2, 4, 8, 5, 10, 9, 7, 3, 6)
        try:
            my_sum = sum([weight * int(digit) for weight,
                         digit in zip(egn_weights, egn)])
            return int(egn[-1]) == my_sum % 11 % 10
        except ValueError:
            return False

    def check_greg_adopt(egn_date):
        # Gregorian calendar adoption: 31/03/1916 > +13 days > 14/04/1916
        if (
            egn_date['year'] == 1916 and
            egn_date['month'] == 4 and
            egn_date['day'] <= 13
              ):
            return False
        return True

    egn_date = get_date(egn)

    return (len(egn) == 10 and
            check_valid_code(egn) and
            isinstance(egn_date, dict) and
            check_greg_adopt(egn_date))


def parse(egn):
    '''
        Parse the EGN information and return hash with the values
    '''
    if not validate(egn):
        raise Exception('Invalid EGN')
    egn_hash = {}

    # Parse the date
    egn_hash.update(get_date(egn))

    # Parse the region
    region_num = int(egn[6:9])
    sorted_regions = sorted(egn_regions.items())
    for (key, value) in sorted_regions:
        if key > region_num:
            egn_hash['region_bg'] = value['bg']
            egn_hash['region_en'] = value['en']
            break

    # Parse the gender
    egn_hash['gender'] = 'male'
    if int(egn[8:9]) % 2:
        egn_hash['gender'] = 'female'

    return egn_hash


def parse_args(args):
    '''
        Method to parse the arguments to the program.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--validate", help="Validate EGN",
                        type=int)
    parser.add_argument("-p", "--parse", help="Parse EGN",
                        type=int)
    # Generate
    parser.add_argument("-g", "--generate", help="Generate EGN",
                        action="store_true")
    parser.add_argument("-s", "--sex", help="Sex/gender",
                        type=str, choices=['male', 'female', 'm', 'f'],
                        default=random.choice(['m', 'f']))
    parser.add_argument("-y", "--year", help="Year (between 1800-2099)",
                        type=int, default=random.randint(1800, 2099))
    parser.add_argument("-m", "--month", help="Month (between 1-12)",
                        type=int, default=random.randint(1, 12))
    parser.add_argument("-d", "--day", help="Day (between 1-31)",
                        type=int, default=random.randint(1, 31))
    parser.add_argument("-r", "--region", help="Region (pernik/sofia etc.)",
                        type=str, default=random.choice(['Pernik', 'Sofia']))
    return vars(parser.parse_args(args))


def calc_args(parser):
    '''
        Method to parse the argparse values and return output
    '''

    if 'parse' in parser and parser['parse']:
        validate_egn = str(parser['parse'])
        if not validate(validate_egn):
            print("{} is invalid!".format(validate_egn))
            exit(1)
        print(parse(validate_egn))
    elif 'generate' in parser and parser['generate']:
        print(generate())
    elif 'validate' in parser and parser['validate']:
        validate_egn = str(parser['validate'])
        if validate(validate_egn):
            print("{} is valid!".format(validate_egn))
        else:
            print("{} is invalid!".format(validate_egn))
            exit(1)
    else:
        parse_args({'-h'})


def main():
    '''
        Entry point for the application script
    '''
    if len(sys.argv) > 1:
        parser = parse_args(sys.argv[1:])
        calc_args(parser)
    else:
        parse_args({'-h'})
