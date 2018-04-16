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

    def get_user(self, username=None):
        """Gets all primitives associated with a particular Pinterest user

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

        fields = "id,username,first_name,last_name,bio,created_at,counts,image"
        result = self._io.get("me", {"fields": fields})
        assert 'data' in result

        return User(result['data'], self._io)


if __name__ == "__main__":
    pass
