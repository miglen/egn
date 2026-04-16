# -*- coding: utf-8 -*-
import egn
import datetime
import pytest


def test_parse_invalid():
    ''' Test invalid parsing '''
    with pytest.raises(egn.InvalidEGNError) as exc_info:
        egn.parse('0001011142')
    assert 'Invalid EGN' in str(exc_info.value)
    # InvalidEGNError must be a ValueError so existing callers keep working.
    assert isinstance(exc_info.value, ValueError)


def test_parse_accepts_int():
    ''' parse() must zero-pad ints just like validate() does '''
    result = egn.parse(21010899)
    assert result['egn'] == '0021010899'
    # Month 21 -> +20 offset -> born in 1800-01-01
    assert (result['year'], result['month'], result['day']) == (1800, 1, 1)
    # Sanity: int form yields the same result as the zero-padded string form
    assert result == egn.parse('0021010899')


def test_parse_egn():
    ''' Test valid parsing '''
    my_egn_m = egn.parse('9941011142')
    expected_egn_m = {'year': 2099, 'month': 1, 'day': 1, 'datetime': datetime.datetime(2099, 1, 1, 0, 0),
                      'region_bg': 'Варна', 'region_en': 'Varna', 'region_iso': 'BG-03', 'gender': 'Male',
                      'egn': '9941011142'}
    my_egn_f = egn.parse('1111136273')
    expected_egn_f = {'year': 1911, 'month': 11, 'day': 13, 'datetime': datetime.datetime(1911, 11, 13, 0, 0),
                      'region_bg': 'София', 'region_en': 'Sofia', 'region_iso': 'BG-22', 'gender': 'Female',
                      'egn': '1111136273'}
    assert (my_egn_m, my_egn_f) == (expected_egn_m, expected_egn_f)
