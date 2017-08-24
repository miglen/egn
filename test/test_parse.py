# -*- coding: utf-8 -*-
import egn
import datetime
import pytest


def test_parse_invalid():
    ''' Test invalid parsing '''
    with pytest.raises(Exception) as exc_info:
        egn.parse('0001011142')
        assert exc_info == 'Invalid EGN'


def test_parse_egn():
    ''' Test valid parsing '''
    my_egn_m = egn.parse('9941011142')
    expected_egn_m = {'datetime': datetime.datetime(2099, 1, 1, 0, 0),
                      'gender': 'male', 'year': 2099, 'month': 1,
                      'region_bg': 'Варна', 'region_en': 'Varna', 'day': 1}
    my_egn_f = egn.parse('1111136273')
    expected_egn_f = {'datetime': datetime.datetime(1911, 11, 13, 0, 0),
                      'gender': 'female', 'year': 1911, 'month': 11,
                      'region_bg': 'София',
                      'region_en': 'Sofia', 'day': 13}
    assert (my_egn_m, my_egn_f) == (expected_egn_m, expected_egn_f)
