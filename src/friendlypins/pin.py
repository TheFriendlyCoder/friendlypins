"""Primitives for operating on Pinterest pins"""
import logging
import json
import requests
from friendlypins.headers import Headers


class Pin(object):
    """Abstraction around a Pinterest pin

    :param dict data: Raw Pinterest API data describing a pin
    :param str root_url: URL of the Pinterest REST API
    :param str token: Authentication token for interacting with the API
    """

    def __init__(self, data, root_url, token):
        self._log = logging.getLogger(__name__)
        self._root_url = root_url
        self._token = token
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

    def delete(self):
        """Removes this pin from it's respective board"""
        temp_url = '{0}/pins/{1}/'.format(
            self._root_url,
            self.unique_id)
        temp_url += "?access_token={0}".format(self._token)

        response = requests.delete(temp_url)

        header = Headers(response.headers)
        self._log.debug("Boards query response header %s", header)

        response.raise_for_status()

if __name__ == "__main__":
    pass
