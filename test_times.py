from times import time_range, compute_overlap_time, iss_passes 
from pytest import raises
from unittest.mock import patch
import requests
import mock
import responses

def test_short_large():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
    result = compute_overlap_time(short, large)
    assert result == expected

def test_large_short():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
    result = compute_overlap_time(large, short)
    assert result == expected

def test_no_overlap():
    time_1 = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    time_2 = time_range("2010-01-12 13:00:00", "2010-01-12 14:00:00", 2, 60)
    expected = []
    result = compute_overlap_time(time_1, time_2)
    assert result == expected

def text_overlap():
    time_1 = time_range("2010-01-12 10:00:00", "2010-01-12 14:35:00")
    time_2 = time_range("2010-01-12 13:00:00", "2010-01-12 15:00:00")
    expected = []
    result = compute_overlap_time(time_1, time_2)
    assert result == expected

def test_gaps():
    time_1 = time_range("2010-01-12 10:00:00", "2010-01-12 16:00:00", 2, 120*60)
    time_2 = time_range("2010-01-12 10:00:00", "2010-01-12 16:00:00", 2, 60*60)
    expected = [('2010-01-12 10:00:00', '2010-01-12 12:00:00'), ('2010-01-12 14:00:00', '2010-01-12 16:00:00')]
    result = compute_overlap_time(time_1, time_2)
    assert result == expected

def test_startend():
    time_1 = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    time_2 = time_range("2010-01-12 12:00:00", "2010-01-12 16:00:00", 2, 60)
    expected = []
    result = compute_overlap_time(time_1, time_2)
    assert result == expected

def test_endstart_error():
    with raises(ValueError, match=r"Start time is after the end time."):
        time_range("2010-01-12 13:00:00", "2010-01-12 12:00:00")

def test_interval_error():
    with raises(ValueError, match=r".* number of intervals is not a positive integer.*"):
        time_range("2010-01-12 11:00:00", "2010-01-12 12:00:00", 1.2)

def test_mock_iss():
    response_obj = requests.models.Response()
    response_obj.encoding = 'ascii'
    response_obj._content = b'{"passes": [{"startUTC": 1750904990, "endUTC": 1750905545}]}'
    with mock.patch('requests.get', new=mock.MagicMock(return_value=response_obj)) as mock_get:
        response = iss_passes('mock_url')
        assert response == [['2025-06-26 03:29:50', '2025-06-26 03:39:05']]

@responses.activate
def test_mock_iss_resp():
    responses.add(
        responses.GET,
        'https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/56/0/0/5/50&apiKey=33Q884-HFUV8K-SCS3LG-55CU',
        json = {"passes": [{"startUTC": 1750904990, "endUTC": 1750905545}]},
        status = 200
    )
    response = iss_passes('https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/56/0/0/5/50&apiKey=33Q884-HFUV8K-SCS3LG-55CU')
    assert response == [['2025-06-26 03:29:50', '2025-06-26 03:39:05']]

# @patch.object(requests, 'get')
# def test_mock_iss():
#     response_obj = requests.models.Response()
#     response_obj.encoding = 'ascii'
#     response_obj._content = b'{"passes": [{"startUTC": 1750904990, "endUTC": 1750905545}]}'
    