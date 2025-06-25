from times import time_range, compute_overlap_time 
from pytest import raises

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

def test_error():
    with raises(ValueError, match=r"Start time is after the end time."):
        time_range("2010-01-12 13:00:00", "2010-01-12 12:00:00")

def test_error():
    with raises(ValueError, match=r"Start time is after the end time."):
        time_range("2010-01-12 11:00:00", "2010-01-12 12:00:00", 1.2)