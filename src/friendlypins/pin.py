"""Primitives for operating on Pinterest pins"""
import logging
import json


class Pin(object):
    """Abstraction around a Pinterest pin

    :param dict data: Raw Pinterest API data describing a pin"""

    def __init__(self, data):
        self._log = logging.getLogger(__name__)
        self._data = data

    def __str__(self):
        """String representation of this pin, for debugging purposes

        :rtype: :class:`str`
        """
        return json.dumps(dict(self._data), sort_keys=True, indent=4)

    def __repr__(self):
        """Pin representation in string format

        :rtype: :class:`str`
        """
        return "<{0} ({1})>".format(self.__class__.__name__, self.note)

    @property
    def url(self):
        """Web address for the UI associated with the pin

        :rtype: :class:`str`
        """
        return self._data['url']

    @property
    def note(self):
        """Descriptive text associated with pin

        :rtype: :class:`str`
        """
        return self._data['note']

    @property
    def link(self):
        """Source URL containing the original data for the pin

        :rtype: :class:`str`
        """
        return self._data['link']

    @property
    def unique_id(self):
        """The unique identifier associated with this pin

        :rtype: :class:`int`
        """
        return int(self._data['id'])

    @property
    def media_type(self):
        """Gets descriptor for the type of data stored in the pin's link

        :rtype: :class:`str`
        """
        if 'media' not in self._data:
            return None

        return self._data['media']['type']

if __name__ == "__main__":
    pass
