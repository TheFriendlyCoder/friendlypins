"""Primitives for operating on Pinterest pins"""
import logging
import json


class Thumbnail(object):
    """Abstraction around a Pin's thumbnail"""

    def __init__(self, data):
        """
        Args:
            data (dict): Raw Pinterest API data describing a thumbnail
        """
        self._log = logging.getLogger(__name__)
        self._data = data

    def __str__(self):
        return json.dumps(dict(self._data), sort_keys=True, indent=4)

    def __repr__(self):
        return "<{0} ({1}x{2})>".format(
            self.__class__.__name__,
            self.width,
            self.height)

    @property
    def width(self):
        """int: The width of the thumbnail image, in pixels"""
        return int(self._data['original']['width'])

    @property
    def height(self):
        """int: The height of the thumbnail image, in pixels"""
        return int(self._data['original']['height'])

    @property
    def url(self):
        """str: Source URL where the thumbnail image can be found"""
        return self._data['original']['url']


if __name__ == "__main__":  # pragma: no cover
    pass
