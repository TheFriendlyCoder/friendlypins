"""Primitives for interacting with Pinterest boards"""
import logging
import json

class Board(object):
    """Abstraction around a Pinterest board

    :param dict data: Raw Pinterest API data describing the board
    """

    def __init__(self, data):
        self._log = logging.getLogger(__name__)
        self._data = data

    def __str__(self):
        """String representation of this object, for debugging purposes

        :rtype: :class:`str`
        """
        return json.dumps(dict(self._data), sort_keys=True, indent=4)

    def __repr__(self):
        """Object representation in string format

        :rtype: :class:`str`
        """
        return "<{0} ({1})>".format(self.__class__.__name__, self.name)

    @property
    def unique_id(self):
        """The unique identifier associated with this board

        :rtype: :class:`int`
        """
        return int(self._data['id'])

    @property
    def name(self):
        """The name of the board

        :rtype: :class:`str`
        """
        return self._data['name']

    @property
    def url(self):
        """Web address for the UI associated with the dashboard

        :rtype: :class:`str`
        """
        return self._data['url']

if __name__ == "__main__":
    pass
