# imports
from utils import ResponseMock

import pytest
import requests


# tests
def test_get_tournaments(mocker):
    mocker.patch(
        'requests.get',
        return_value=ResponseMock('tests/mocks/player.html')
    )

    resp = requests.get('https://google.se/')

    print(resp.text)

    assert resp.text == 'yo'
