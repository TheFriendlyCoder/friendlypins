"""Primary entry point for the Friendly Pinterest library"""
from __future__ import print_function
import logging
from friendlypins.user import User
from friendlypins.utils.rest_io import RestIO


class API(object):  # pylint: disable=too-few-public-methods
    """High level abstraction for the core Pinterest API

    :param str personal_access_token:
            API authentication token used for secure access to a users'
            Pinterest data
    """

    def __init__(self, personal_access_token):
        self._log = logging.getLogger(__name__)
        self._io = RestIO(personal_access_token)

    @property
    def user(self):
        """Gets all primitives associated with the authenticated user
        :returns: currently authenticated pinterest user
        :rtype: :class:`friendlypins.user.User`
        """
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
        """Gets the time when the next refresh for API queries takes effect

        :rtype: :class:`datetime.datetime`
        """
        try:
            if self._io.headers is None:
                self._io.get("me")
        finally:
            return self._io.headers.time_to_refresh  # pylint: disable=lost-exception

    @property
    def transaction_limit(self):
        """Gets the total number of transactions per hour we're allotted

        :rtype: :class:`int`
        """
        try:
            if self._io.headers is None:
                self._io.get("me")
        finally:
            return self._io.headers.rate_limit  # pylint: disable=lost-exception

    @property
    def transaction_remaining(self):
        """Gets the total number of transactions per hour we're allotted

        :rtype: :class:`int`
        """
        try:
            if self._io.headers is None:
                self._io.get("me")
        finally:
            return self._io.headers.rate_remaining  # pylint: disable=lost-exception

if __name__ == "__main__":
    pass
