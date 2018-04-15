"""Primary entry point for the Friendly Pinterest library"""
from __future__ import print_function
import logging
import requests
from friendlypins.user import User
from friendlypins.headers import Headers

class API(object):  # pylint: disable=too-few-public-methods
    """High level abstraction for the core Pinterest API

    :param str personal_access_token:
            API authentication token used for secure access to a users'
            Pinterest data
    """

    # URL of the root namespace for the Pinterest API
    _root_url = 'https://api.pinterest.com/v1'

    def __init__(self, personal_access_token):
        self._log = logging.getLogger(__name__)
        self._token = personal_access_token

    def get_user(self, username=None):
        """Gets all primitives associated with a particular Pinterst user

        :param str username:
            Optional name of a user to look up
            If not provided, the currently authentcated user will be returned

        :returns: Pinterest user with the given name
        :rtype: :class:`friendlypins.user.User`
        """
        self._log.debug("Getting authenticated user details...")
        if username:
            raise NotImplementedError(
                "Querying arbitrary Pinerest users is not yet supported.")
        else:
            temp_url = "{0}/me".format(self._root_url)
        temp_url += "?access_token={0}".format(self._token)
        temp_url += "&fields=id,username,first_name,last_name,bio,created_at,counts,image"
        response = requests.get(temp_url)
        response.raise_for_status()

        header = Headers(response.headers)
        self._log.debug("Getting user query response: %s", header)

        raw = response.json()

        assert 'data' in raw

        return User(raw['data'], self._root_url, self._token)


# pylint: disable-all
if __name__ == "__main__":
    pass
