"""Primitives for operating on Pinterest pins"""
import logging
import json


class Thumbnail(object):
    """Abstraction around a Pin's thumbnail

    :param dict data: Raw Pinterest API data describing a thumbnail
    :param str root_url: URL of the Pinterest REST API
    :param str token: Authentication token for interacting with the API
    """

    def __init__(self, data):
        self._log = logging.getLogger(__name__)
        self._data = data

    def __str__(self):
        """String representation of this thumbnail, for debugging purposes

        :rtype: :class:`str`
        """
        return json.dumps(dict(self._data), sort_keys=True, indent=4)

    def __repr__(self):
        """Thumbnail representation in string format

        :rtype: :class:`str`
        """
        return "<{0} ({1}x{2})>".format(
            self.__class__.__name__,
            self.width,
            self.height)

    @property
    def width(self):
        """The width of the thumbnail image, in pixels

        :rtype: :class:`int`
        """
        return int(self._data['original']['width'])

    @property
    def height(self):
        """The height of the thumbnail image, in pixels

        :rtype: :class:`int`
        """
        return int(self._data['original']['height'])

    @property
    def url(self):
        """Source URL where the thumbnail image can be found

        :rtype: :class:`str`
        """
        return self._data['original']['url']


if __name__ == "__main__":
    pass
