# -*- coding: utf-8 -*-
import egn
import sys
import datetime
import pytest


def test_generation():
    ''' Test generation produces valid egn '''
    assert egn.validate(egn.generate())


def test_generation_options():
    ''' Test generation produce valid egn with options '''
    assert egn.validate(egn.generate(region=1, sex=1, day=1, month=1,
                        year=2000, limit=100))


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
