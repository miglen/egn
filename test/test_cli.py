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


def test_cli_random(capsys):
    ''' --random produces N valid EGNs '''
    egn_options = {'random': True, 'limit': 3, 'region': 'Sofia', 'gender': 'm'}
    egn.calc_args(egn_options)
    out, _ = capsys.readouterr()
    lines = [line for line in out.strip().split('\n') if line]
    assert len(lines) == 3
    for line in lines:
        assert egn.validate(line)
        assert egn.parse(line)['region_iso'] == 'BG-22'


def test_cli_random_no_limit_defaults_to_ten(capsys):
    ''' --random without --limit must fall back to 10 (not crash on None) '''
    egn_options = {'random': True, 'limit': None, 'region': None, 'gender': None}
    egn.calc_args(egn_options)
    out, _ = capsys.readouterr()
    lines = [line for line in out.strip().split('\n') if line]
    assert len(lines) == 10


def test_main_no_args_prints_help(capsys, monkeypatch):
    ''' Running `egn` with no args prints help and exits '''
    monkeypatch.setattr('sys.argv', ['egn'])
    with pytest.raises(SystemExit):
        egn.main()
    out, _ = capsys.readouterr()
    assert 'usage' in out.lower()


def test_main_with_args_dispatches(capsys, monkeypatch):
    ''' main() with argv forwards to calc_args '''
    monkeypatch.setattr('sys.argv', ['egn', '-v', '0021010899'])
    egn.main()
    out, _ = capsys.readouterr()
    assert '0021010899 is valid!' in out


def test_cli_unknown_option_prints_help(capsys):
    '''
    calc_args() with a dict that doesn't match any command falls through to
    the help path.
    '''
    with pytest.raises(SystemExit):
        egn.calc_args({'something': 'else'})
