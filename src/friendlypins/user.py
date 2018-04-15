"""Interfaces for interacting with Pinterest users"""
import logging
import json
import requests
from friendlypins.board import Board
from friendlypins.headers import Headers


class User(object):
    """Abstraction around a Pinterest user and their associated data

    :param dict data: JSON data parsed from the API
    :param str root_url: URL of the Pinterest REST API
    :param str token: Authentication token for interacting with the API
    """

    def __init__(self, data, root_url, token):
        self._log = logging.getLogger(__name__)
        self._data = data
        self._root_url = root_url
        self._token = token

    def __str__(self):
        """String representation of this user, for debugging purposes

        :rtype: :class:`str`
        """
        return json.dumps(dict(self._data), sort_keys=True, indent=4)

    def __repr__(self):
        """User representation in string format

        :rtype: :class:`str`
        """
        return "<{0} ({1} {2})>".format(
            self.__class__.__name__,
            self.first_name,
            self.last_name)

    @property
    def unique_id(self):
        """Gets the internal unique ID associated with the user

        :rtype: :class:`int`
        """
        return int(self._data['id'])

    @property
    def first_name(self):
        """Gets the first name of the user

        :rtype: :class:`str`
        """
        return self._data['first_name']

    @property
    def last_name(self):
        """Gets the last name of the user

        :rtype: :class:`str`
        """
        return self._data['last_name']

    @property
    def name(self):
        """Gets the name of the user

        alias for first_name + last_name

        :rtype: :class:`str`
        """
        return "{0} {1}".format(self.first_name, self.last_name)

    @property
    def url(self):
        """Gets the URL of the users profile

        :rtype: :class:`str`
        """
        return self._data['url']

    @property
    def boards(self):
        """Gets a list of boards owned by this user

        :rtype: :class:`list` of :class:`friendlypins.board.Board`
        """
        self._log.debug("Loading boards for user %s...", self.name)

        temp_url = '{0}/me/boards/'.format(self._root_url)
        temp_url += "?access_token={0}".format(self._token)
        response = requests.get(temp_url)

        header = Headers(response.headers)
        self._log.debug("Boards query response header %s", header)

        response.raise_for_status()
        raw = response.json()
        assert 'data' in raw

        retval = []
        for cur_item in raw['data']:
            retval.append(Board(cur_item, self._root_url, self._token))
        return retval

if __name__ == "__main__":
    pass
