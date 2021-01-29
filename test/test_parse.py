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
    expected_egn_m = {'year': 2099, 'month': 1, 'day': 1, 'datetime': datetime.datetime(2099, 1, 1, 0, 0),
                      'region_bg': 'Варна', 'region_en': 'Varna', 'region_iso': 'BG-03', 'gender': 'Male',
                      'egn': '9941011142'}
    my_egn_f = egn.parse('1111136273')
    expected_egn_f = {'year': 1911, 'month': 11, 'day': 13, 'datetime': datetime.datetime(1911, 11, 13, 0, 0),
                      'region_bg': 'София', 'region_en': 'Sofia', 'region_iso': 'BG-22', 'gender': 'Female',
                      'egn': '1111136273'}
    assert (my_egn_m, my_egn_f) == (expected_egn_m, expected_egn_f)
