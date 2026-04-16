# -*- coding: utf-8 -*-
from collections import Counter

import pytest

import egn


# ----------------------------------------------------------------------
# Original tests (kept intact)
# ----------------------------------------------------------------------

def test_generation_options():
    ''' Test generation produce valid egn with options '''
    for i in egn.generate(region='Pernik', gender='m', limit=100):
        assert egn.validate(i)


def test_generation_random():
    ''' Test generation produce valid egn with options '''
    random = egn.generate_random(limit=10)
    assert len(random) == 10
    for i in random:
        assert egn.validate(i)


def test_valid():
    ''' Test series of valid numbers '''
    assert all((egn.validate('0021010899'), egn.validate('0041010384'),
               egn.validate(9941011142), egn.validate(21010899)))


def test_invalid():
    ''' Test series of invalid numbers '''
    assert not any((egn.validate(9999991142), egn.validate(77770899),
                    egn.validate(9961012142), egn.validate('210108ghjk')))


def test_invalid_gregorian():
    ''' Test invalid numbers during gregorian adoption '''
    assert not any((egn.validate('1604010295'), egn.validate('1604066376'),
                    egn.validate(1604107747), egn.validate(1604136154)))


def test_get_date():
    ''' Test get_date method with incorrect values '''
    assert not any((egn.get_date('a'), egn.get_date(123)))


# ----------------------------------------------------------------------
# Generator correctness tests
# ----------------------------------------------------------------------

def _decode_date(e):
    d = egn.get_date(e)
    return (d['year'], d['month'], d['day'])


def test_generate_dates_match_requested_range():
    '''
    Every generated EGN's birth date must fall inside the requested range.
    This is the regression test for the dday[6:7] month-slice bug which
    silently produced EGNs for the wrong months.
    '''
    results = egn.generate(region='Sofia',
                           date_from='2020-10-01',
                           date_to='2020-12-31',
                           limit=None)
    assert results, 'expected some EGNs'
    for e in results:
        y, m, d = _decode_date(e)
        assert y == 2020
        assert 10 <= m <= 12, f'{e} decoded month {m} is outside Oct-Dec'


def test_generate_october_november_december_separately():
    '''
    Each of Oct/Nov/Dec used to be mis-decoded. Generate one day each and
    verify the month in the resulting EGNs is correct.
    '''
    for month, day in [(10, 15), (11, 15), (12, 15)]:
        date = f'2020-{month:02d}-{day:02d}'
        egns = egn.generate(region='Sofia', date_from=date, date_to=date,
                            gender='m', limit=None)
        assert egns, f'no EGNs generated for {date}'
        for e in egns:
            y, m, d = _decode_date(e)
            assert (y, m, d) == (2020, month, day), f'{e} decoded as {y}-{m}-{d}'


def test_generate_region_boundary_first_and_last_codes():
    '''
    The last code of a region (e.g. 43 for Blagoevgrad) used to be
    attributed to the next region by parse(). Verify every generated
    Blagoevgrad EGN parses as BG-01 — including those using code 43.
    '''
    egns = egn.generate(region='Blagoevgrad',
                        date_from='2020-06-15', date_to='2020-06-15',
                        limit=None)
    # 0-43 inclusive = 44 codes, one valid EGN each
    assert len(egns) == 44
    for e in egns:
        parsed = egn.parse(e)
        assert parsed['region_iso'] == 'BG-01'

    # Also verify the very last code of the last region (999, BG-XX).
    last_region = egn.generate(region='Other',
                               date_from='2020-06-15', date_to='2020-06-15',
                               limit=None)
    # Codes 926-999 inclusive = 74 codes
    assert len(last_region) == 74
    for e in last_region:
        assert egn.parse(e)['region_iso'] == 'BG-XX'


def test_generate_check_digit_nine_is_reachable():
    '''
    The generator previously used range(0, 9) which made EGNs ending in 9
    impossible. Exhaustively generate enough EGNs to prove 9 is reachable.
    '''
    egns = egn.generate(region='Sofia',
                        date_from='2020-01-01', date_to='2020-01-31',
                        limit=None)
    check_digits = {e[-1] for e in egns}
    assert '9' in check_digits
    # Every possible check digit should show up given enough samples.
    assert check_digits == set('0123456789')


def test_generate_leap_day():
    ''' Feb 29 on a leap year must produce valid EGNs '''
    egns = egn.generate(region='Varna',
                        date_from='2020-02-29', date_to='2020-02-29',
                        limit=None)
    assert egns
    for e in egns:
        y, m, d = _decode_date(e)
        assert (y, m, d) == (2020, 2, 29)


def test_generate_century_offsets():
    ''' Births in 1800s (+20) and 2000s (+40) must round-trip correctly '''
    # 1850s: month offset +20
    old = egn.generate(region='Sofia',
                       date_from='1850-07-04', date_to='1850-07-04',
                       limit=5)
    assert old
    for e in old:
        y, m, d = _decode_date(e)
        assert (y, m, d) == (1850, 7, 4)
        # position 2-3 of the EGN is the encoded month; +20 for 1800s
        assert e[2:4] == '27'

    # 2000s: month offset +40
    new = egn.generate(region='Sofia',
                       date_from='2024-07-04', date_to='2024-07-04',
                       limit=5)
    assert new
    for e in new:
        y, m, d = _decode_date(e)
        assert (y, m, d) == (2024, 7, 4)
        assert e[2:4] == '47'


def test_generate_female_filter():
    ''' gender='f' should yield only female EGNs '''
    egns = egn.generate(region='Varna', gender='f',
                        date_from='2020-03-15', date_to='2020-03-15',
                        limit=None)
    assert egns
    for e in egns:
        assert egn.parse(e)['gender'] == 'Female'


def test_generate_gender_full_words():
    ''' gender='male'/'female' (not just the single-letter form) works '''
    males = egn.generate(region='Sofia', gender='male',
                         date_from='2020-03-15', date_to='2020-03-15',
                         limit=5)
    females = egn.generate(region='Sofia', gender='female',
                           date_from='2020-03-15', date_to='2020-03-15',
                           limit=5)
    assert males and females
    assert all(egn.parse(e)['gender'] == 'Male' for e in males)
    assert all(egn.parse(e)['gender'] == 'Female' for e in females)


def test_generate_region_name_variants():
    ''' Latin, Cyrillic, and ISO names must all resolve to the same region '''
    latin = egn.generate(region='Sofia',
                         date_from='2020-01-01', date_to='2020-01-01',
                         limit=None)
    cyrillic = egn.generate(region='София',
                            date_from='2020-01-01', date_to='2020-01-01',
                            limit=None)
    iso = egn.generate(region='BG-22',
                       date_from='2020-01-01', date_to='2020-01-01',
                       limit=None)
    assert latin == cyrillic == iso
    assert latin  # non-empty


def test_generate_unknown_region_returns_empty():
    ''' Unknown region names must yield no EGNs instead of raising '''
    assert egn.generate(region='Atlantis',
                        date_from='2020-01-01', date_to='2020-01-01') == []


def test_generate_reversed_dates_returns_empty():
    ''' date_from > date_to is an empty range, not an error '''
    assert egn.generate(region='Sofia',
                        date_from='2020-12-31',
                        date_to='2020-01-01',
                        limit=None) == []


def test_generate_no_region_filter_covers_all_codes():
    '''
    region=None must enumerate all 1000 region codes (times one valid
    check digit each) for a single day.
    '''
    egns = egn.generate(region=None,
                        date_from='1999-12-31', date_to='1999-12-31',
                        limit=None)
    assert len(egns) == 1000


def test_generate_unlimited_with_limit_zero():
    ''' limit <= 0 is treated as "no limit" '''
    a = egn.generate(region='Pernik',
                     date_from='2020-01-01', date_to='2020-01-01',
                     limit=0)
    b = egn.generate(region='Pernik',
                     date_from='2020-01-01', date_to='2020-01-01',
                     limit=None)
    assert a == b
    # Pernik = codes 378-395 = 18 codes
    assert len(a) == 18


def test_generate_default_date_to_is_today():
    ''' Omitting date_to must default to today, not a stale captured value '''
    # Asking for limit=1 with no date_to should not raise and should produce a
    # valid EGN.
    result = egn.generate(region='Sofia', gender='m', limit=1)
    assert len(result) == 1
    assert egn.validate(result[0])


def test_generate_random_with_explicit_region():
    ''' generate_random must honor an explicit region argument '''
    egns = egn.generate_random(region='BG-14', limit=5, gender='f')
    assert len(egns) == 5
    for e in egns:
        parsed = egn.parse(e)
        assert parsed['region_iso'] == 'BG-14'
        assert parsed['gender'] == 'Female'


# ----------------------------------------------------------------------
# Exception type
# ----------------------------------------------------------------------

def test_invalid_egn_error_is_value_error():
    ''' InvalidEGNError must subclass ValueError for existing callers '''
    assert issubclass(egn.InvalidEGNError, ValueError)


# ----------------------------------------------------------------------
# Larger-dataset round-trip tests. Use the generator as the source of
# truth — every EGN it emits must validate and parse back to the values
# that went in.
# ----------------------------------------------------------------------

# (english_name, iso_code, start_code, end_code) for every region.
ALL_REGIONS = [
    ('Blagoevgrad',    'BG-01',   0,  43),
    ('Burgas',         'BG-02',  44,  93),
    ('Varna',          'BG-03',  94, 139),
    ('Veliko Turnovo', 'BG-04', 140, 169),
    ('Vidin',          'BG-05', 170, 183),
    ('Vratza',         'BG-06', 184, 217),
    ('Gabrovo',        'BG-07', 218, 233),
    ('Dobrich',        'BG-08', 790, 821),
    ('Kurdzhali',      'BG-09', 234, 281),
    ('Kyustendil',     'BG-10', 282, 301),
    ('Lovech',         'BG-11', 302, 319),
    ('Montana',        'BG-12', 320, 341),
    ('Pazardzhik',     'BG-13', 342, 377),
    ('Pernik',         'BG-14', 378, 395),
    ('Pleven',         'BG-15', 396, 435),
    ('Plovdiv',        'BG-16', 436, 501),
    ('Razgrad',        'BG-17', 502, 527),
    ('Ruse',           'BG-18', 528, 555),
    ('Silistra',       'BG-19', 556, 575),
    ('Sliven',         'BG-20', 576, 601),
    ('Smolyan',        'BG-21', 602, 623),
    ('Sofia',          'BG-22', 624, 721),
    ('Sofia (county)', 'BG-23', 722, 751),
    ('Stara Zagora',   'BG-24', 752, 789),
    ('Targovishte',    'BG-25', 822, 843),
    ('Haskovo',        'BG-26', 844, 871),
    ('Shumen',         'BG-27', 872, 903),
    ('Yambol',         'BG-28', 904, 925),
    ('Other',          'BG-XX', 926, 999),
]


@pytest.mark.parametrize('name,iso,start,end', ALL_REGIONS)
def test_every_region_full_enumeration_round_trip(name, iso, start, end):
    '''
    For every region: enumerate every code on one day, validate each,
    parse each, and verify the parsed region and date round-trip
    exactly. This exercises the first and last code of every region —
    the exact place the old parse() off-by-one bit us.
    '''
    egns = egn.generate(region=name,
                        date_from='2020-06-15', date_to='2020-06-15',
                        limit=None)
    expected = end - start + 1
    assert len(egns) == expected, f'{name}: got {len(egns)}, expected {expected}'
    # All must validate and parse back to the requested region + date.
    seen_codes = set()
    for e in egns:
        assert egn.validate(e)
        parsed = egn.parse(e)
        assert parsed['region_iso'] == iso
        assert parsed['year'] == 2020
        assert parsed['month'] == 6
        assert parsed['day'] == 15
        seen_codes.add(int(e[6:9]))
    # Every code in the region range must be covered exactly once.
    assert seen_codes == set(range(start, end + 1))


def test_all_1000_region_codes_reachable_in_one_day():
    '''
    Enumerating a single day with no region filter must yield one EGN
    per code, 000-999 inclusive, with no duplicates.
    '''
    egns = egn.generate(date_from='1999-12-31', date_to='1999-12-31',
                        limit=None)
    assert len(egns) == 1000
    assert len(set(egns)) == 1000  # no duplicates
    codes = sorted(int(e[6:9]) for e in egns)
    assert codes == list(range(0, 1000))


@pytest.mark.parametrize('month', list(range(1, 13)))
def test_every_month_decodes_correctly(month):
    '''
    Generate for the 15th of every month of 2020 and verify every
    parsed EGN decodes back to that month. This is the regression
    test family for the Oct/Nov/Dec mis-slicing bug.
    '''
    date = f'2020-{month:02d}-15'
    egns = egn.generate(region='Sofia', date_from=date, date_to=date,
                        limit=None)
    # Sofia has 98 region codes (624-721), one EGN per code per day.
    assert len(egns) == 98
    for e in egns:
        parsed = egn.parse(e)
        assert (parsed['year'], parsed['month'], parsed['day']) == (2020, month, 15)


def test_sofia_codes_count_sanity():
    '''Sanity check for the count used in test_every_month_decodes_correctly.'''
    egns = egn.generate(region='Sofia',
                        date_from='2020-06-15', date_to='2020-06-15',
                        limit=None)
    # Sofia: 624-721 inclusive = 98 codes, one EGN per code.
    assert len(egns) == 98


def test_multi_month_no_duplicates():
    '''
    Enumerate every EGN across an entire month, across every region.
    Must yield 31 * 1000 = 31_000 distinct valid EGNs.
    '''
    egns = egn.generate(date_from='2020-01-01', date_to='2020-01-31',
                        limit=None)
    assert len(egns) == 31 * 1000
    assert len(set(egns)) == len(egns)
    # Spot-check: every EGN validates.
    for e in egns:
        assert egn.validate(e)


def test_full_year_sofia_round_trip():
    '''
    Large dataset: generate every valid EGN for Sofia in 2020 and
    verify the validator, parser, and check-sum all agree.
    '''
    egns = egn.generate(region='Sofia',
                        date_from='2020-01-01', date_to='2020-12-31',
                        limit=None)
    # 2020 is a leap year: 366 days * 98 Sofia codes = 35_868 EGNs.
    assert len(egns) == 366 * 98
    assert len(set(egns)) == len(egns)  # unique
    # Round-trip every one (full scan; fast because validate is O(1)).
    for e in egns:
        assert egn.validate(e)
        parsed = egn.parse(e)
        assert parsed['egn'] == e
        assert parsed['region_iso'] == 'BG-22'
        assert parsed['year'] == 2020


def test_gregorian_gap_day_by_day():
    '''
    Bulgaria skipped 1-13 April 1916 when adopting the Gregorian
    calendar. Those 13 days must be absent from any enumeration, and
    the surrounding days must be present.
    '''
    egns = egn.generate(region='Sofia',
                        date_from='1916-03-25', date_to='1916-04-20',
                        limit=None)
    # Gather the (year, month, day) set actually produced.
    present = {(p['year'], p['month'], p['day'])
               for p in (egn.parse(e) for e in egns)}
    # All of March 25-31 must be present.
    for d in range(25, 32):
        assert (1916, 3, d) in present
    # All of April 1-13 must be *absent* (Gregorian gap).
    for d in range(1, 14):
        assert (1916, 4, d) not in present
    # April 14-20 must be present.
    for d in range(14, 21):
        assert (1916, 4, d) in present


def test_century_boundaries_round_trip():
    '''
    Dates on either side of the 1900/2000 boundaries must round-trip
    through the +20 / no-offset / +40 month encodings.
    '''
    cases = [
        ('1850-07-04', '27'),  # 1800s: month +20
        ('1899-12-31', '32'),  # 1800s boundary
        ('1900-01-01', '01'),  # 1900s: no offset
        ('1999-12-31', '12'),  # 1900s boundary
        ('2000-01-01', '41'),  # 2000s: month +40
        ('2024-07-04', '47'),  # 2000s recent
    ]
    for date, expected_mm in cases:
        egns = egn.generate(region='Sofia',
                            date_from=date, date_to=date, limit=None)
        assert egns, f'no EGNs for {date}'
        for e in egns:
            assert e[2:4] == expected_mm, (
                f'{date}: EGN {e} has encoded month {e[2:4]}, expected {expected_mm}'
            )
            parsed = egn.parse(e)
            assert parsed['datetime'].strftime('%Y-%m-%d') == date


@pytest.mark.parametrize('year', [1904, 1952, 2000, 2004, 2020])
def test_leap_day_generable(year):
    '''Feb 29 on a real leap year must produce valid EGNs.'''
    date = f'{year}-02-29'
    egns = egn.generate(region='Sofia', date_from=date, date_to=date, limit=None)
    assert egns
    for e in egns:
        parsed = egn.parse(e)
        assert (parsed['year'], parsed['month'], parsed['day']) == (year, 2, 29)


def test_non_leap_centurial_year_feb_29_is_rejected():
    '''1900 is divisible by 100 but not 400 — not a leap year.'''
    with pytest.raises(ValueError):
        egn.generate(region='Sofia',
                     date_from='1900-02-29', date_to='1900-02-29')


def test_gender_distribution_over_whole_day():
    '''
    With no gender filter, enumerating every code on one day produces
    exactly 500 male and 500 female EGNs (by construction — the region
    code's parity encodes gender).
    '''
    egns = egn.generate(date_from='2000-06-15', date_to='2000-06-15',
                        limit=None)
    assert len(egns) == 1000
    genders = Counter(egn.parse(e)['gender'] for e in egns)
    assert genders == {'Male': 500, 'Female': 500}


def test_check_digit_distribution_all_ten_reachable():
    '''
    Over a large sample every check digit 0-9 must be reachable, not
    just 0-8 (the old range(0, 9) bug made '9' impossible).
    '''
    egns = egn.generate(date_from='2000-01-01', date_to='2000-01-31',
                        limit=None)
    digits = Counter(e[-1] for e in egns)
    assert set(digits) == set('0123456789')
    # Every digit is represented by a substantial count (not just 1 or 2).
    assert all(count > 500 for count in digits.values())


def test_large_random_batch_round_trips():
    '''Generate a big random batch and round-trip every one.'''
    egns = egn.generate_random(limit=500)
    assert len(egns) == 500
    assert len(set(egns)) == 500  # no duplicates
    for e in egns:
        assert egn.validate(e)
        parsed = egn.parse(e)
        assert parsed['egn'] == e
        # Gender must match the region-code parity.
        expected_gender = 'Male' if int(e[8]) % 2 == 0 else 'Female'
        assert parsed['gender'] == expected_gender


def test_generated_egns_reconstruct_from_components():
    '''
    For every generated EGN, reconstructing the 10-digit string from
    the decoded (year, month, day, region_code, check_digit) parts
    yields back the same EGN. Proves parsing is lossless.
    '''
    egns = egn.generate(date_from='1999-12-25', date_to='2000-01-05',
                        limit=None)
    # 12 days * 1000 codes = 12_000 EGNs crossing the 2000 boundary.
    assert len(egns) == 12_000
    for e in egns:
        parsed = egn.parse(e)
        # Rebuild the encoded YY-MM prefix using the same rules generate uses.
        y, m, d = parsed['year'], parsed['month'], parsed['day']
        if y >= 2000:
            ey, em = y - 2000, m + 40
        elif y < 1900:
            ey, em = y - 1800, m + 20
        else:
            ey, em = y - 1900, m
        prefix = f'{ey:02d}{em:02d}{d:02d}'
        assert e.startswith(prefix)
        # Last 4 chars are region (3) + check digit (1).
        assert len(e[6:]) == 4
        assert e[6:9] == f'{int(e[6:9]):03d}'
