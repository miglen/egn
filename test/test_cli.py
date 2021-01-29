# -*- coding: utf-8 -*-
import egn
import pytest


def test_cli_invalid_parse(capsys):
    ''' Test invalid parsing via cli '''
    with pytest.raises(SystemExit):
        egn_options = {'parse': 9999991142}
        egn.calc_args(egn_options)
        out, err = capsys.readouterr()
        assert out == "9999991142 is invalid!\n"


def test_cli_parse(capsys):
    ''' Test valid number parsing via cli '''
    egn_options = {'parse': 9941011142}
    egn.calc_args(egn_options)
    out, err = capsys.readouterr()
    assert ('Varna' in out and '2099' in out and 'Male' in out)


def test_cli_generate(capsys):
    ''' Test generate via cli '''
    egn_options = {'generate': True, 'limit': 1, 'region': 'Sofia', 'gender': 'm',
                   'from': '2020-01-01', 'to': '2020-12-12'}
    egn.calc_args(egn_options)
    out, err = capsys.readouterr()
    assert egn.validate(out.strip()) is True


def test_cli_validation(capsys):
    ''' Test validation via cli '''
    egn_options = {'validate': '0021010899'}
    egn.calc_args(egn_options)
    out, err = capsys.readouterr()
    assert out == "0021010899 is valid!\n"


def test_cli_validation_ivalid(capsys):
    ''' Test invalid validation via cli '''
    egn_options = {'validate': '0021010892'}
    with pytest.raises(SystemExit):
        egn.calc_args(egn_options)
        out, err = capsys.readouterr()
        assert out == "0021010892 is invalid!\n"


def test_cli_invalid_params(capsys):
    ''' Test cli with invalid params '''
    egn_options = {'something': 'invalid'}
    with pytest.raises(SystemExit):
        egn.calc_args(egn_options)
        out, err = capsys.readouterr()
        assert out == "usage*"


def test_cli_main(capsys):
    ''' Test main entry point '''
    with pytest.raises(SystemExit):
        egn.main()
        out, err = capsys.readouterr()
        assert out == "usage*"
