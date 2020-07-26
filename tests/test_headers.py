from datetime import datetime
import pytest
from friendlypins.utils.rest_io import RestIO
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


@pytest.mark.vcr()
def test_headers_properties(test_env):
    obj = RestIO(test_env["key"])
    headers = obj.headers
    assert isinstance(headers.date, datetime)
    assert headers.date.tzinfo == tz.tzlocal()
    assert isinstance(headers.rate_limit, int)
    assert headers.rate_limit == 1
    assert isinstance(headers.rate_remaining, int)
    assert isinstance(headers.percent_rate_remaining, int)
    assert isinstance(headers.time_to_refresh, datetime)
    assert headers.time_to_refresh.tzinfo == tz.tzlocal()


@pytest.mark.vcr()
def test_rate_limit_exceeded(test_env):
    obj = RestIO(test_env["key"])

    # Wait for our request limit to get reached
    headers = obj.headers
    while headers.rate_remaining > 0:
        obj.refresh_headers()
        headers = obj.headers

    assert headers.rate_remaining == 0
    assert headers.percent_rate_remaining == 0


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
    expected_time = datetime(year=2018, month=3, day=31, hour=10, minute=58, second=39, tzinfo=tz.tzutc())
    assert tmp == expected_time
