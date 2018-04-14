"""Primitives for interacting with Pinterest boards"""
import logging
import json
import requests
from friendlypins.headers import Headers
from friendlypins.pin import Pin


class Board(object):
    """Abstraction around a Pinterest board

    :param dict data: Raw Pinterest API data describing the board
    :param str root_url: URL of the Pinterest REST API
    :param str token: Authentication token for the REST API
    """

    def __init__(self, data, root_url, token):
        self._log = logging.getLogger(__name__)
        self._data = data
        self._root_url = root_url
        self._token = token

    def __str__(self):
        """String representation of this board, for debugging purposes

        :rtype: :class:`str`
        """
        return json.dumps(dict(self._data), sort_keys=True, indent=4)

    def __repr__(self):
        """Board representation in string format

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

    @property
    def all_pins(self):
        """Gets a list of all pins from this board

        NOTE: This process may take a long time to complete and require
        a lot of memory for boards that contain large numbers of pins

        :rtype: :class:`list` of :class:`friendlypins.pin.Pin`
        """
        temp_url = '{0}/boards/{1}/pins/'.format(self._root_url, self.unique_id)
        temp_url += "?access_token={0}".format(self._token)
        temp_url += "&limit=100"
        temp_url += "&fields=id,image,metadata,link,url,original_link,media"
        response = requests.get(temp_url)
        response.raise_for_status()
        retval = []
        header = Headers(response.headers)
        self._log.debug("Pins query response header %s", header)

        while True:
            raw = response.json()
            assert 'data' in raw

            for cur_item in raw['data']:
                retval.append(Pin(cur_item, self._root_url, self._token))

            self._log.debug("Raw keys are %s", raw.keys())
            self._log.debug("Paged info is %s", raw['page'])
            if not raw['page']['cursor']:
                break

            paged_url = temp_url + "&cursor={0}".format(raw['page']['cursor'])
            response = requests.get(paged_url)
            response.raise_for_status()
            header = Headers(response.headers)
            self._log.debug("Pins query response header %s", header)

        return retval

if __name__ == "__main__":
    pass
