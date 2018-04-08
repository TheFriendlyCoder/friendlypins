"""Primitives for operation in HTTP response headers provided by Pinterest"""
from datetime import datetime
import json
from dateutil import tz

class Headers(object):
    """Abstraction around the Pinterest API HTTP response header

    :param dict data: Header data parsed from the HTTP response
    """
    def __init__(self, data):
        self._data = data

    def __str__(self):
        """String representation of the header data

        :rtype: :class:`str`
        """
        return json.dumps(dict(self._data), sort_keys=True, indent=4)

    @property
    def rate_limit(self):
        """number of API requests in total permitted for the authenticated user

        :rtype: :class:`int`
        """
        return int(self._data['X-Ratelimit-Limit'])

    @property
    def rate_remaining(self):
        """Number of API requests the authenticated user is allowed to make

        The remaining number of requests resets every hour, according to
        the API docs

        :rtype: :class:`int`
        """
        return int(self._data['X-Ratelimit-Remaining'])

    @property
    def percent_rate_remaining(self):
        """Gets a percentage representation of the number of API requests left

        See :meth:`rate_remaining` for more info

        :rtype: :class:`int`
        """
        percent = float(self.rate_remaining) / float(self.rate_limit)
        return int(percent * 100)

    @property
    def date(self):
        """Date/time when this header was last populated

        :rtype: :class:`datetime.datetime`
        """
        #TBD: Confirm if time encoding is 12h or 24h
        # parse dateimte string
        parsed_date = \
            datetime.strptime(self._data['Date'], "%a, %d %b %Y %H:%M:%S %Z")

        # Sanity Check: typically our response data should have dates
        # encoded in GMT time zone... but in the off chance Pinterest changes
        # their APIs in the future, we check just to be sure and return the
        # default formatted date object
        if "GMT" not in self._data['Date']:  # pragma: no cover
            return parsed_date

        # overload time zone info since it's ignored by datetime apparently
        date_with_tz = parsed_date.replace(tzinfo=tz.tzutc())

        # return time data in current locale for convenience
        return date_with_tz.astimezone(tz.tzlocal())

if __name__ == "__main__":
    pass
