# imports
from .utils import ResponseMock

from badmintonswedenapi.utils import get_soup


# tests
def test_get_soup(mocker):
    mocker.patch(
        'requests.get',
        return_value=ResponseMock('tests/unit_tests/mocks/utils/github.html')
    )

    soup = get_soup('https://github.com/')

    assert soup is not None

    assert soup.findAll('label', {'for': 'user[email]'})[0].text == 'Email'
