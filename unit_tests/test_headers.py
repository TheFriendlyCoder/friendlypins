import pytest
import mock
from friendlypins.headers import Headers
from dateutil import tz

sample_rate_limit = "200"
sample_rate_max = "150"
sample_header = {
      'Access-Control-Allow-Origin': '*',
      'Age': '0',
      'Cache-Control': 'private',
      'Content-Encoding': 'gzip',
      'Content-Type': 'application/json',
      'Pinterest-Version': 'e3f92ef',
      'X-Content-Type-Options': 'nosniff',
      'X-Pinterest-RID': '12345678',
      'X-Ratelimit-Limit': sample_rate_limit,
      'X-Ratelimit-Remaining': sample_rate_max,
      'Transfer-Encoding': 'chunked',
      'Date': 'Sat, 31 Mar 2018 10:58:09 GMT',
      'Connection': 'keep-alive',
      'Pinterest-Generated-By': ''
    }


def test_get_date_locale():
    obj = Headers(sample_header)

    assert obj.date.tzinfo == tz.tzlocal()

def test_get_rate_limit():
    obj = Headers(sample_header)

    assert obj.rate_limit == 200

def test_get_rate_max():
    obj = Headers(sample_header)

    assert obj.rate_remaining == 150

def test_get_rate_percent():
    obj = Headers(sample_header)

    assert obj.percent_rate_remaining == 75


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])