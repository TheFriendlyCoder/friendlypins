"""Interfaces for interacting with Pinterest users"""
import logging

class User(object):
    """Abstraction around a Pinterest user and their associated data"""

    def __init__(self, data):
        """Constructor

        :param dict data: JSON data parsed from the API
        """
        self._log = logging.getLogger(__name__)
        self._data = data

    @property
    def unique_id(self):
        """Gets the internal unique ID associated with the user
        :rtype: :class:`str`
        """
        return self._data['id']

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
    def url(self):
        """Gets the URL of the users profile
        :rtype: :class:`str`
        """
        return self._data['url']

if __name__ == "__main__":
    pass
