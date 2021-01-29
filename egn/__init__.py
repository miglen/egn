# -*- coding: utf-8 -*-
import argparse
import sys
import random
from datetime import timedelta, datetime
import json

egn_regions = {
    # https://www.iso.org/obp/ui/#iso:code:3166:BG
    43: {'bg': 'Благоевград', 'en': 'Blagoevgrad', 'start': 0, 'iso': 'BG-01'},  # 000 - 043
    93: {'bg': 'Бургас', 'en': 'Burgas', 'start': 44, 'iso': 'BG-02'},  # 044 - 093
    139: {'bg': 'Варна', 'en': 'Varna', 'start': 94, 'iso': 'BG-03'},  # 094 - 139
    169: {'bg': 'Велико Търново', 'en': 'Veliko Turnovo', 'start': 140, 'iso': 'BG-04'},  # 140 - 169
    183: {'bg': 'Видин', 'en': 'Vidin', 'start': 170, 'iso': 'BG-05'},  # 170 - 183
    217: {'bg': 'Враца', 'en': 'Vratza', 'start': 184, 'iso': 'BG-06'},  # 184 - 217
    233: {'bg': 'Габрово', 'en': 'Gabrovo', 'start': 218, 'iso': 'BG-07'},  # 218 - 233
    281: {'bg': 'Кърджали', 'en': 'Kurdzhali', 'start': 234, 'iso': 'BG-09'},  # 234 - 281
    301: {'bg': 'Кюстендил', 'en': 'Kyustendil', 'start': 282, 'iso': 'BG-10'},  # 282 - 301
    319: {'bg': 'Ловеч', 'en': 'Lovech', 'start': 302, 'iso': 'BG-11'},  # 302 - 319
    341: {'bg': 'Монтана', 'en': 'Montana', 'start': 320, 'iso': 'BG-12'},  # 320 - 341
    377: {'bg': 'Пазарджик', 'en': 'Pazardzhik', 'start': 342, 'iso': 'BG-13'},  # 342 - 377
    395: {'bg': 'Перник', 'en': 'Pernik', 'start': 378, 'iso': 'BG-14'},  # 378 - 395
    435: {'bg': 'Плевен', 'en': 'Pleven', 'start': 396, 'iso': 'BG-15'},  # 396 - 435
    501: {'bg': 'Пловдив', 'en': 'Plovdiv', 'start': 436, 'iso': 'BG-16'},  # 436 - 501
    527: {'bg': 'Разград', 'en': 'Razgrad', 'start': 502, 'iso': 'BG-17'},  # 502 - 527
    555: {'bg': 'Русе', 'en': 'Ruse', 'start': 528, 'iso': 'BG-18'},  # 528 - 555
    575: {'bg': 'Силистра', 'en': 'Silistra', 'start': 556, 'iso': 'BG-19'},  # 556 - 575
    601: {'bg': 'Сливен', 'en': 'Sliven', 'start': 576, 'iso': 'BG-20'},  # 576 - 601
    623: {'bg': 'Смолян', 'en': 'Smolyan', 'start': 602, 'iso': 'BG-21'},  # 602 - 623
    721: {'bg': 'София', 'en': 'Sofia', 'start': 624, 'iso': 'BG-22'},  # 624 - 721
    751: {'bg': 'София (окръг)', 'en': 'Sofia (county)', 'start': 722, 'iso': 'BG-23'},  # 722 - 751
    789: {'bg': 'Стара Загора', 'en': 'Stara Zagora', 'start': 752, 'iso': 'BG-24'},  # 752 - 789
    821: {'bg': 'Добрич', 'en': 'Dobrich', 'start': 790, 'iso': 'BG-08'},  # 790 - 821
    843: {'bg': 'Търговище', 'en': 'Targovishte', 'start': 822, 'iso': 'BG-25'},  # 822 - 843
    871: {'bg': 'Хасково', 'en': 'Haskovo', 'start': 844, 'iso': 'BG-26'},  # 844 - 871
    903: {'bg': 'Шумен', 'en': 'Shumen', 'start': 872, 'iso': 'BG-27'},  # 872 - 903
    925: {'bg': 'Ямбол', 'en': 'Yambol', 'start': 904, 'iso': 'BG-28'},  # 904 - 925
    999: {'bg': 'Друг', 'en': 'Other', 'start': 926, 'iso': 'BG-XX'}}  # 926 - 999


def generate_random(gender=None,
                    region=None,
                    limit=10):
    """
    Generate a random EGN.
    """
    egns = []
    while len(egns) < limit:
        if region is None:
            rr = random.randint(1, 28)
            rand_region = f"BG-{rr:02d}"
        else:
            rand_region = region
        year = random.randint(1800, datetime.today().year - 1)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        date_from = f"{year}-{month}-{day}"
        date_to = datetime.today().strftime('%Y-%m-%d')
        rand_egn = generate(date_from=date_from, date_to=date_to, region=rand_region, gender=gender, limit=1)
        if len(rand_egn) == 1:
            egns.append(rand_egn[0])
    return egns


def generate(date_from="1800-01-01",
             date_to=datetime.today().strftime('%Y-%m-%d'),
             gender=None,
             region=None,
             limit=10):
    """
    Generate egn within boundaries.
    """
    def get_region_range(region="Other"):
        """
        Get region code.
        Region could be the latin, cyrrilic or ISO 3166 anotation of the region.
        """
        start = 0
        end = 0
        for i in egn_regions:
            if region.lower() in [egn_regions[i]['en'].lower(),
                                  egn_regions[i]['bg'].lower(),
                                  egn_regions[i]['iso'].lower()]:
                start = egn_regions[i]['start']
                end = i
        return start, end

    def get_dates_range(date_from, date_to, limit=None):
        """
            Generate all dates between date range in ENG suitable format.
            Params in ISO 8601 format.
        """
        dates = []
        try:
            sdate = datetime.strptime(date_from, '%Y-%m-%d')
            edate = datetime.strptime(date_to, '%Y-%m-%d')
            delta = edate - sdate

            for i in range(delta.days + 1):
                if limit is not None and i > limit:
                    return dates
                dday = str(sdate + timedelta(days=i))
                year, month, day = int(dday[0:4]), int(dday[6:7]), int(dday[8:10])
                if year >= 2000:
                    month += 40
                    year -= 2000
                elif year < 1900:
                    month += 20
                    year -= 1800
                else:
                    # Gregorian calendar adoption: 31/03/1916 > +13 days > 14/04/1916
                    if year == 1916 and month == 4 and day <= 13:
                        continue
                    year -= 1900
                dates.append(f"{year:02d}{month:02d}{day:02d}")
            return dates
        except Exception as e:
            print(e)
            return None

    egns = []
    if not region:
        regions = range(0, 999, 1)
    else:
        region_start, region_end = get_region_range(region)
        regions = range(region_start, region_end, 1)

    if gender is not None:
        if gender[0].lower() == 'm':  # Male
            regions = [x for x in regions if x % 2 == 0]
        else:  # Female
            regions = [x for x in regions if x % 2]

    regions = [f"{x:02d}" for x in regions]
    dates = get_dates_range(date_from, date_to, limit=limit)
    counter = 1

    # Generate the list of egns
    for dt in dates:
        for region in regions:
            for check_num in range(0, 9, 1):
                egene = f"{dt}{region}{check_num}"
                if validate(egene):
                    counter += 1
                    egns.append(egene)
                    if counter > limit:
                        return egns
    return egns


def get_date(egn):
    '''
        Get the date information from the EGN
        Return hash with year, month, day and datetime.
    '''
    from datetime import datetime
    try:
        year, month, day = int(egn[0:2]), int(egn[2:4]), int(egn[4:6])
    except Exception:
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
    egn = str(egn)
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
            egn_hash['region_iso'] = value['iso']
            break

    # Parse the gender
    egn_hash['gender'] = 'Male'
    if int(egn[8:9]) % 2:
        egn_hash['gender'] = 'Female'

    egn_hash['egn'] = egn

    return egn_hash


def parse_args(args):
    '''
        Method to parse the arguments to the program.
    '''
    parser = argparse.ArgumentParser()
    today = format(datetime.today().strftime('%Y-%m-%d'))
    parser.add_argument("-v", "--validate", help="Validate EGN", type=str)
    parser.add_argument("-p", "--parse", help="Parse EGN", type=str)
    # Generation
    parser.add_argument("-l", "--limit", help="Limit of generated results (default: 1)", type=int, default=1)
    parser.add_argument("-r", "--random", help="Generate random EGN (default limit: 1)", action="store_true")
    parser.add_argument("-g", "--generate", help="Generate EGN", action="store_true")
    parser.add_argument("--gender", help="Gender - Male or Female", type=str, choices=['m', 'f'])
    parser.add_argument("--region", help="Region (Latin/Cyrrilic region name or ISO 3166 format)", type=str)
    parser.add_argument("--from", help="Date from generate (Y-m-d) (default: 1800-01-01)",
                        type=str, default='1800-01-01')
    parser.add_argument("--to", type=str, help=f"Date to generate (Y-m-d) (default: {today})", default=today)
    return vars(parser.parse_args(args))


def calc_args(parser):
    '''
        Method to parse the argparse values and return an output.
    '''

    if 'parse' in parser and parser['parse']:
        validate_egn = str(parser['parse'])
        if not validate(validate_egn):
            print("{} is invalid!".format(validate_egn))
            exit(1)
        validate_egn = parse(validate_egn)
        validate_egn.pop('datetime')
        print(json.dumps(validate_egn))
    elif 'random' in parser and parser['random']:
        print("\n".join(generate_random(limit=parser['limit'], region=parser['region'], gender=parser['gender'])))
    elif 'generate' in parser and parser['generate']:
        print("\n".join(generate(limit=parser['limit'], region=parser['region'], gender=parser['gender'],
                                 date_from=parser['from'],  date_to=parser['to'])))
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
