import pytest
import mock
from friendlypins.headers import Headers
from dateutil import tz

sample_rate_limit = 200
sample_rate_max = 150
sample_content_length = 1024
header_date = 'Sat, 31 Mar 2018 10:58:09 GMT'
sample_header = {
      'Access-Control-Allow-Origin': '*',
      'Age': '0',
      'Cache-Control': 'private',
      'Content-Encoding': 'gzip',
      'Content-Type': 'application/json',
      'Pinterest-Version': 'e3f92ef',
      'X-Content-Type-Options': 'nosniff',
      'X-Pinterest-RID': '12345678',
      'X-Ratelimit-Limit': str(sample_rate_limit),
      'X-Ratelimit-Remaining': str(sample_rate_max),
      'Transfer-Encoding': 'chunked',
      'Date': header_date,
      'X-Ratelimit-Refresh': "30",
      'Connection': 'keep-alive',
      'Pinterest-Generated-By': '',
      'Content-Length': str(sample_content_length)
    }


def test_get_date_locale():
    obj = Headers(sample_header)

    assert obj.date.tzinfo == tz.tzlocal()

def test_get_rate_limit():
    obj = Headers(sample_header)

    assert obj.rate_limit == sample_rate_limit

def test_get_rate_max():
    obj = Headers(sample_header)

    assert obj.rate_remaining == sample_rate_max

def test_get_rate_percent():
    obj = Headers(sample_header)

    assert obj.percent_rate_remaining == 75

def test_get_num_bytes():
    obj = Headers(sample_header)

    assert obj.bytes == sample_content_length

def test_time_to_refresh():

    obj = Headers(sample_header)
    tmp = obj.time_to_refresh
    expected_time_str = 'Sat, 31 Mar 2018 10:58:39'

    tmp = tmp.astimezone(tz.tzutc())
    assert tmp.strftime("%a, %d %b %Y %H:%M:%S") == expected_time_str
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])