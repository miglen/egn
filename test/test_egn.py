import egn


def test_generation():
    assert egn.validate(egn.generate())


def test_valid():
    assert all((egn.validate('0021010899'), egn.validate('0041010384'),
               egn.validate(9941011142), egn.validate(21010899)))
