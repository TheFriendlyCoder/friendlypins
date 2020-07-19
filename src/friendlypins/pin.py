"""Primitives for operating on Pinterest pins"""
import logging
import json
from friendlypins.thumbnail import Thumbnail


class Pin(object):
    """Abstraction around a Pinterest pin"""

    def __init__(self, data, rest_io):
        """
        Args:
            data (dict): Raw Pinterest API data describing a pin
            rest_io (RestIO): reference to the Pinterest REST API
        """
        self._log = logging.getLogger(__name__)
        self._io = rest_io
        self._data = data

    def __str__(self):
        return json.dumps(dict(self._data), sort_keys=True, indent=4)

    def __repr__(self):
        return "<{0} ({1})>".format(self.__class__.__name__, self.note)

    @property
    def url(self):
        """str: Web address for the UI associated with the pin"""
        return self._data['url']

    @property
    def note(self):
        """str: Descriptive text associated with pin"""
        return self._data['note']

    @property
    def link(self):
        """str: Source URL containing the original data for the pin"""
        return self._data['link']

    @property
    def unique_id(self):
        """int: The unique identifier associated with this pin"""
        return int(self._data['id'])

    @property
    def media_type(self):
        """str: descriptor for the type of data stored in the pin's link

        Returns None if the type of data associated with the Pin
        is unknown
        """
        if 'media' not in self._data:
            return None

        return self._data['media']['type']

    @property
    def thumbnail(self):
        """Thumbnail: the thumbnail image associated with this pin"""
        assert 'image' in self._data
        return Thumbnail(self._data['image'])

    def delete(self):
        """Removes this pin from it's respective board"""
        self._log.debug('Deleting pin %s', repr(self))
        self._io.delete('pins/{0}'.format(self.unique_id))


if __name__ == "__main__":  # pragma: no cover
    pass
