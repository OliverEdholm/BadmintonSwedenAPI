# imports
from utils import get_soup


def test_get_soup():
    soup = get_soup('https://github.com/')

    assert soup is not None
