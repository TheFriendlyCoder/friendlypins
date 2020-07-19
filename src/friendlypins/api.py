"""Primary entry point for the Friendly Pinterest library"""
from __future__ import print_function
import logging
from friendlypins.user import User
from friendlypins.utils.rest_io import RestIO


class API(object):  # pylint: disable=too-few-public-methods
    """High level abstraction for the core Pinterest API"""

    def __init__(self, personal_access_token):
        """
        Args:
            personal_access_token (str):
                API authentication token used for secure access to a users'
                Pinterest data
        """
        self._log = logging.getLogger(__name__)
        self._io = RestIO(personal_access_token)

    @property
    def user(self):
        """User: Gets all primitives associated with the authenticated user"""
        self._log.debug("Getting authenticated user details...")

        fields = ",".join([
            "id",
            "username",
            "first_name",
            "last_name",
            "bio",
            "created_at",
            "counts",
            "image",
            "account_type",
            "url"
        ])
        result = self._io.get("me", {"fields": fields})
        assert 'data' in result

        return User(result['data'], self._io)

    @property
    def rate_limit_refresh(self):
        """datetime.datetime: Gets the time when the next refresh for API
        queries takes effect"""
        return self._io.headers.time_to_refresh

    @property
    def transaction_limit(self):
        """int: Gets the total number of transactions per hour we're allotted
        """
        return self._io.headers.rate_limit

    @property
    def transaction_remaining(self):
        """int: Gets the total number of transactions per hour we're allotted
        """
        return self._io.headers.rate_remaining


if __name__ == "__main__":  # pragma: no cover
    pass
