"""Primitives for interacting with Pinterest boards"""
import logging
import json
from friendlypins.pin import Pin


class Board(object):
    """Abstraction around a Pinterest board

    :param dict data: Raw Pinterest API data describing the board
    :param rest_io: reference to the Pinterest REST API
    :type rest_io: :class:`friendlypins.utils.rest_io.RestIO`
    """

    def __init__(self, data, rest_io):
        self._log = logging.getLogger(__name__)
        self._data = data
        self._io = rest_io

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
    def num_pins(self):
        """Gets the total number of pins linked to this board

        :rtype: :class:`int`
        """
        return int(self._data['counts']['pins'])

    @property
    def all_pins(self):
        """Gets a list of all pins from this board

        NOTE: This process may take a long time to complete and require
        a lot of memory for boards that contain large numbers of pins

        :rtype: :class:`list` of :class:`friendlypins.pin.Pin`
        """
        self._log.debug('Gettings all pins for board %s...', self.name)
        retval = list()

        properties = {
            "fields": ','.join([
                "id",
                "link",
                "url",
                "creator",
                "board",
                "created_at",
                "note,color",
                "counts",
                "media",
                "attribution",
                "image",
                "metadata",
                "original_link"
            ])
        }

        while True:
            result = self._io.get(
                "boards/{0}/pins".format(self.unique_id),
                properties)
            assert 'data' in result

            for cur_item in result['data']:
                retval.append(Pin(cur_item, self._io))
            if not result["page"]["cursor"]:
                break
            properties["cursor"] = result["page"]["cursor"]

        return retval


if __name__ == "__main__":
    pass
