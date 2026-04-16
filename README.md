# egn

[![PyPI package](https://badge.fury.io/py/egn.svg)](https://pypi.python.org/pypi/egn)
[![Build Status](https://github.com/miglen/egn/actions/workflows/python-package.yml/badge.svg)](https://github.com/miglen/egn/actions)
[![Documentation Status](https://readthedocs.org/projects/egn/badge/?version=latest)](http://egn.readthedocs.io/en/latest/?badge=latest)
[![Coverage](https://img.shields.io/codecov/c/github/miglen/egn.svg)](http://codecov.io/gh/miglen/egn)

A Python library and command-line tool for **validating**, **parsing** and
**generating** the Bulgarian Unified Civil Number (ЕГН / EGN — *Единен граждански номер*).

*Библиотека и команден ред на Python за **проверка**, **анализ** и
**генериране** на български Единни граждански номера (ЕГН).*

---

## Table of contents / Съдържание

- [What is an EGN?](#what-is-an-egn--какво-е-егн)
- [Installation / Инсталация](#installation--инсталация)
- [Python API](#python-api)
  - [`validate`](#validateegn)
  - [`parse`](#parseegn)
  - [`get_date`](#get_dateegn)
  - [`generate`](#generatedate_from-date_to-gender-region-limit)
  - [`generate_random`](#generate_randomgender-region-limit)
- [Command-line interface / Команден ред](#command-line-interface--команден-ред)
- [Regions / Области](#regions--области)
- [Algorithm / Алгоритъм](#algorithm--алгоритъм)
- [Development / Разработка](#development--разработка)
- [License / Лиценз](#license--лиценз)

---

## What is an EGN? / Какво е ЕГН?

**English.** The EGN (*Unified Civil Number*) is a 10-digit identifier
assigned to every Bulgarian citizen and to every foreign resident. It
encodes:

| Positions | Meaning                                                                                            |
|-----------|----------------------------------------------------------------------------------------------------|
| 1–2       | Year of birth (last two digits)                                                                    |
| 3–4       | Month of birth, with a century offset: `+20` for births in the 1800s, `+40` for births after 2000 |
| 5–6       | Day of birth                                                                                       |
| 7–9       | Regional code (0 – 999), assigned by the civil registry and reflecting the place of registration   |
| 9         | The last digit of the regional code also encodes the sex: **even = male**, **odd = female**        |
| 10        | Check digit (mod-11 / mod-10 weighted checksum)                                                    |

**Български.** ЕГН-то е 10-цифрен идентификатор, съдържащ датата на
раждане, район на регистрация, пол и контролна цифра. Месецът е
кодиран с добавени `+20` за рождени през XIX век и `+40` за рождени
след 2000 г. Полът се определя от последната цифра на кода на
областта: **четна → мъж**, **нечетна → жена**.

> **Note / Забележка.** Dates between **1 April 1916 and 13 April 1916**
> do not exist — Bulgaria adopted the Gregorian calendar by skipping
> those 13 days. EGNs carrying such dates are considered invalid by
> this library.

---

## Installation / Инсталация

```bash
pip install egn
```

Supported Python: **3.6+** (the library uses f-strings).

---

## Python API

```python
import egn
```

### `validate(egn)`

Return `True` if `egn` is a valid EGN, `False` otherwise.
Accepts either a `str` or an `int` (ints are zero-padded to 10 digits).

*Връща `True`, ако ЕГН-то е валидно.*

```python
>>> egn.validate('0021010899')
True
>>> egn.validate(21010899)        # int, will be zero-padded
True
>>> egn.validate('1234567890')
False
```

### `parse(egn)`

Return a `dict` describing the EGN. Raises `Exception('Invalid EGN')`
if the input is invalid.

*Връща речник с данните, извлечени от ЕГН-то.*

```python
>>> egn.parse('1111136273')
{
    'year': 1911,
    'month': 11,
    'day': 13,
    'datetime': datetime.datetime(1911, 11, 13, 0, 0),
    'region_bg': 'София',
    'region_en': 'Sofia',
    'region_iso': 'BG-22',
    'gender': 'Female',
    'egn': '1111136273',
}
```

### `get_date(egn)`

Return just the date portion of an EGN (decoded `year`, `month`, `day`
and a `datetime`). Returns `False` for malformed input.

```python
>>> egn.get_date('9941011142')
{'year': 2099, 'month': 1, 'day': 1, 'datetime': datetime.datetime(2099, 1, 1, 0, 0)}
```

### `generate(date_from, date_to, gender, region, limit)`

Deterministically enumerate valid EGNs matching the given constraints.
**All parameters are optional** and can be mixed freely.

*Генерира всички валидни ЕГН-та, които отговарят на зададените филтри.
Всички параметри са по избор и могат да се комбинират.*

| Parameter   | Type                    | Default       | Meaning                                                                              |
|-------------|-------------------------|---------------|--------------------------------------------------------------------------------------|
| `date_from` | `str` (`YYYY-MM-DD`)    | `'1800-01-01'`| Earliest date of birth to enumerate.                                                 |
| `date_to`   | `str` (`YYYY-MM-DD`)    | today         | Latest date of birth to enumerate.                                                   |
| `gender`    | `'m'` / `'male'` / `'f'`/ `'female'` | `None` | Filter by sex. `None` returns both.                                                  |
| `region`    | `str`                   | `None`        | Region name in Latin, Cyrillic or ISO 3166-2 (e.g. `'Sofia'`, `'София'`, `'BG-22'`). `None` returns every region. |
| `limit`     | `int` / `None`          | `10`          | Maximum number of EGNs to return. **Pass `None` to enumerate every combination.**    |

Examples:

```python
# All EGNs for men born in Sofia on 2020-10-15.
egn.generate(region='Sofia', gender='m',
             date_from='2020-10-15', date_to='2020-10-15',
             limit=None)
# -> 49 EGNs (one per even region code in 624-721)

# All female EGNs in Burgas across January 2020.
egn.generate(region='Burgas', gender='f',
             date_from='2020-01-01', date_to='2020-01-31',
             limit=None)

# Every EGN for a single day regardless of region or gender.
egn.generate(date_from='1999-12-31', date_to='1999-12-31', limit=None)
# -> 1000 EGNs (one per region code 000-999)

# Using Cyrillic or ISO region names.
egn.generate(region='Пловдив', limit=5)
egn.generate(region='BG-16',   limit=5)
```

How partial inputs compose:

| `date_from`/`date_to` | `gender` | `region` | `limit` | Result                                               |
|-----------------------|----------|----------|---------|------------------------------------------------------|
| date range            | any      | any      | `N`     | First `N` EGNs in the range, all regions, both sexes |
| single day            | `'m'`    | any      | `None`  | Every male EGN born that day, across all regions     |
| date range            | any      | `'Varna'`| `None`  | Every EGN born in Varna during the range             |
| date range            | `'f'`    | `'BG-22'`| `None`  | Every female EGN born in Sofia in the range          |

### `generate_random(gender, region, limit)`

Return `limit` random valid EGNs. Each EGN has a uniformly random date
between 1800-01-01 and yesterday and a uniformly random region (or the
one you specified).

*Генерира произволни ЕГН-та.*

```python
>>> egn.generate_random(limit=3, region='Varna', gender='f')
['8841020217', '2643026019', '5424077115']
```

---

## Command-line interface / Команден ред

After installation the `egn` command is available:

```bash
# Validate
$ egn -v 0021010899
0021010899 is valid!

# Parse (prints JSON)
$ egn -p 9941011142
{"year": 2099, "month": 1, "day": 1, "region_bg": "Варна", ...}

# Generate with full filter set
$ egn -g --from 2020-10-15 --to 2020-10-15 --region Sofia --gender m
# -> prints 49 EGNs, one per line

# Generate — omit --limit to enumerate every combination
$ egn -g --from 2020-01-01 --to 2020-01-01 --region Pernik
# -> prints all 18 EGNs for that day and region

# Generate with a cap
$ egn -g --from 2020-01-01 --to 2020-12-31 --region Burgas --limit 100

# Random EGNs
$ egn -r --limit 5
$ egn -r --region Пловдив --gender f --limit 3
```

Flags:

| Flag              | Purpose                                                                    |
|-------------------|-----------------------------------------------------------------------------|
| `-v EGN`          | Validate a single EGN.                                                      |
| `-p EGN`          | Parse a single EGN and print JSON.                                          |
| `-g`              | Generate EGNs matching the given filters.                                   |
| `-r`              | Generate random EGNs.                                                       |
| `-l N` / `--limit N` | Cap the number of results. **Omit with `-g` to enumerate every combination.** |
| `--gender m/f`    | Filter by sex.                                                              |
| `--region NAME`   | Latin, Cyrillic, or ISO 3166-2 region name.                                 |
| `--from DATE`     | ISO date `YYYY-MM-DD`. Default `1800-01-01`.                                |
| `--to DATE`       | ISO date `YYYY-MM-DD`. Default: today.                                      |

---

## Regions / Области

The regional code in positions 7–9 of the EGN maps to one of 29
administrative regions. The library ships with the full table, keyed
by ISO 3166-2 code, Bulgarian name, and English transliteration.

*Библиотеката съдържа пълната таблица на 29-те области, като
търсенето работи с латиница, кирилица или ISO 3166-2 код.*

| ISO     | English         | Български       | Code range |
|---------|-----------------|-----------------|------------|
| BG-01   | Blagoevgrad     | Благоевград     | 000–043    |
| BG-02   | Burgas          | Бургас          | 044–093    |
| BG-03   | Varna           | Варна           | 094–139    |
| BG-04   | Veliko Turnovo  | Велико Търново  | 140–169    |
| BG-05   | Vidin           | Видин           | 170–183    |
| BG-06   | Vratza          | Враца           | 184–217    |
| BG-07   | Gabrovo         | Габрово         | 218–233    |
| BG-08   | Dobrich         | Добрич          | 790–821    |
| BG-09   | Kurdzhali       | Кърджали        | 234–281    |
| BG-10   | Kyustendil      | Кюстендил       | 282–301    |
| BG-11   | Lovech          | Ловеч           | 302–319    |
| BG-12   | Montana         | Монтана         | 320–341    |
| BG-13   | Pazardzhik      | Пазарджик       | 342–377    |
| BG-14   | Pernik          | Перник          | 378–395    |
| BG-15   | Pleven          | Плевен          | 396–435    |
| BG-16   | Plovdiv         | Пловдив         | 436–501    |
| BG-17   | Razgrad         | Разград         | 502–527    |
| BG-18   | Ruse            | Русе            | 528–555    |
| BG-19   | Silistra        | Силистра        | 556–575    |
| BG-20   | Sliven          | Сливен          | 576–601    |
| BG-21   | Smolyan         | Смолян          | 602–623    |
| BG-22   | Sofia           | София           | 624–721    |
| BG-23   | Sofia (county)  | София (окръг)   | 722–751    |
| BG-24   | Stara Zagora    | Стара Загора    | 752–789    |
| BG-25   | Targovishte     | Търговище       | 822–843    |
| BG-26   | Haskovo         | Хасково         | 844–871    |
| BG-27   | Shumen          | Шумен           | 872–903    |
| BG-28   | Yambol          | Ямбол           | 904–925    |
| BG-XX   | Other           | Друг            | 926–999    |

---

## Algorithm / Алгоритъм

The checksum in position 10 is computed from the first 9 digits using
the weights `(2, 4, 8, 5, 10, 9, 7, 3, 6)`:

```
checksum = (sum(weight_i * digit_i for i in 1..9) mod 11) mod 10
```

If that value equals the 10th digit, the EGN is well-formed. The
library additionally verifies that positions 1–6 decode to a real
calendar date, that the date is not inside the 1–13 April 1916
Gregorian gap, and that the regional code is in range.

Reference: <http://www.grao.bg/esgraon.html#section2>

---

## Development / Разработка

```bash
git clone https://github.com/miglen/egn.git
cd egn
python3 -m venv .venv && source .venv/bin/activate
pip install -e . pytest
pytest test/
```

Contributions welcome. Please include a test case with any bug fix or
new feature.

*Приноси са добре дошли. Моля, добавяйте тест за всяка корекция или
нова възможност.*

---

## License / Лиценз

GNU General Public License v3.0 — see [LICENSE](LICENSE).
