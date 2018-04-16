"""Primitives for operating on Pinterest pins"""
import logging
import json
from friendlypins.thumbnail import Thumbnail


class Pin(object):
    """Abstraction around a Pinterest pin

    :param dict data: Raw Pinterest API data describing a pin
    :param rest_io: reference to the Pinterest REST API
    :type rest_io: :class:`friendlypins.utils.rest_io.RestIO`
    """

    def __init__(self, data, rest_io):
        self._log = logging.getLogger(__name__)
        self._io = rest_io
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

        Returns None if the type of data associated with the Pin
        is unknown

        :rtype: :class:`str`
        """
        if 'media' not in self._data:
            return None

        return self._data['media']['type']

    @property
    def thumbnail(self):
        """Gets the thumbnail image associated with this pin

        :rtype: :class:`friendlypins.thumbnail.Thumbnail`
        """
        assert 'image' in self._data
        return Thumbnail(self._data['image'])

    def delete(self):
        """Removes this pin from it's respective board"""
        self._log.debug('Deleting pin %s', repr(self))
        self._io.delete('pins/{0}'.format(self.unique_id))


if __name__ == "__main__":
    pass
