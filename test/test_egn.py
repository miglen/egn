# -*- coding: utf-8 -*-
import egn
import datetime
import pytest


def test_generation():
    assert egn.validate(egn.generate())


def test_generation_withparams():
    assert egn.validate(egn.generate(region=1, sex=1, day=1, month=1,
                        year=2000, limit=100))


def test_valid():
    assert all((egn.validate('0021010899'), egn.validate('0041010384'),
               egn.validate(9941011142), egn.validate(21010899)))


def test_invalid_region():
    assert egn.validate('0001011142') is False


def test_invalid_gregorian():
    assert not any((egn.validate('1604010295'), egn.validate('1604066376'),
                    egn.validate(1604107747), egn.validate(1604136154)))


def test_get_date():
    assert not any((egn.get_date('a'), egn.get_date(123)))


def test_parse():
    my_egn = egn.parse('9941011142')
    expected_egn = {'datetime': datetime.datetime(2099, 1, 1, 0, 0),
                    'gender': 'male', 'year': 2099, 'month': 1,
                    'region_bg': 'Варна', 'region_en': 'Varna', 'day': 1}
    assert my_egn == expected_egn


def test_parse_invalid():
        with pytest.raises(Exception) as exc_info:
            egn.parse('0001011142')
            assert exc_info == 'Invalid EGN'
