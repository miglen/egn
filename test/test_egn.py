# -*- coding: utf-8 -*-
import egn


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
