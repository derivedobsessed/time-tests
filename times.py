import datetime
import requests
import json


def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_s = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    if start_time_s > end_time_s:
        raise ValueError("Start time is after the end time.")
    # try: 
    #     number_of_intervals = int(number_of_intervals)
    # except ValueError:
    #     raise ValueError('The number of intervals is not a number.')
    if type(number_of_intervals) is not int and number_of_intervals > 0:
        raise ValueError(f"The number of intervals is not a positive integer. You put in {number_of_intervals}!!!")
    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1)
    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                  start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                 for i in range(number_of_intervals)]
    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range]


def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            low = max(start1, start2)
            high = min(end1, end2)
            if high > low:
                overlap_time.append((low, high))
    return overlap_time

def iss_passes(url):
    response=requests.get(url)
    #response_text=json.loads(response.text)
    response_text = response.json()
    passes=response_text['passes']

    times=[]
    for p in passes:
        start_unix, end_unix = p['startUTC'], p['endUTC']
        start, end = datetime.datetime.fromtimestamp(start_unix), datetime.datetime.fromtimestamp(end_unix)
        times.append([start.strftime("%Y-%m-%d %H:%M:%S"),end.strftime("%Y-%m-%d %H:%M:%S")])
    return times

if __name__ == "__main__":
    # large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    # short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    # print(compute_overlap_time(large, short))
    print(iss_passes('https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/56/0/0/5/50&apiKey=33Q884-HFUV8K-SCS3LG-55CU'))
    