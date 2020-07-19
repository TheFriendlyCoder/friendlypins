"""custom exceptions provided by our library"""
from datetime import datetime
from dateutil import tz
from humanize import naturaltime
from requests.exceptions import HTTPError
from friendlypins.headers import Headers


class RateLimitException(HTTPError):
    """Helper class for extrapolating details about a rate limit error"""
    def __init__(self, response):
        super().__init__(response=response)

    @property
    def pin_headers(self):
        """Headers: reference to the pre-parsed HTTP headers returned from
        the API"""
        return Headers(self.response.headers)

    @property
    def rate_renewal(self):
        """datetime.datetime: time, in the current locale, when requests will
        be allowed once again"""
        return self.pin_headers.time_to_refresh

    @property
    def friendly_error(self):
        """str: user friendly representation of the error message"""
        time_to_renew = self.rate_renewal - datetime.now(tz=tz.tzutc())
        fmt = naturaltime(time_to_renew.total_seconds(), future=True)
        return "Rate limit reached. Try again " + fmt
