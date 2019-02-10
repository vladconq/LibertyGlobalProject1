import pytest
from person import Person


@pytest.fixture()  # make instance before tests
def some_person():
    return Person('vlad', 1996, 'lenina')


# Let's test init block of Person!

def test_set_init_name(some_person):
    assert some_person.name == 'vlad'


def test_set_init_address(some_person):
    assert some_person.address == 'lenina'


def test_set_init_age(some_person):
    assert some_person.yob == 1996


# Let's test setting blocks in Person!

@pytest.mark.parametrize('inp, out', [
    ('', ''),
    ('vladislav', 'vladislav'),
])
def test_set_name(some_person, inp, out):
    some_person.set_name(inp)
    assert some_person.name == out  # find a bug: AssertionError


@pytest.mark.parametrize('inp, out', [
    ('', ''),
    ('kosmonavtov', 'kosmonavtov'),
])
def test_set_address(some_person, inp, out):
    some_person.set_address(inp)
    assert some_person.address == out  # find a bug: AssertionError


# Let's test getting blocks in Person!

@pytest.mark.parametrize('inp, out', [
    (1996, 23),
])
def test_get_age(some_person, inp, out):
    assert some_person.get_age() == out  # find a bug: name 'datetime' is not defined; reverse subtraction order


@pytest.mark.parametrize('name, expected', [
    ('vlad', 'vlad'),
    ('', ''),
])
def test_get_name(some_person, name, expected):
    some_person.name = name
    assert some_person.get_name() == expected


# Let's test boolean function in Person!

@pytest.mark.parametrize('address, expected', [
    ('karla marksa', False),
    (None, True),
    ('', True)
])
def test_is_homeless(some_person, address, expected):
    some_person.address = address
    assert some_person.is_homeless() is expected  # find a bug: address instead of self.address; None without ''
