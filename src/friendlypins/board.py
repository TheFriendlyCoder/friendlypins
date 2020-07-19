"""Primitives for interacting with Pinterest boards"""
import logging
import json
from friendlypins.pin import Pin


class Board(object):
    """Abstraction around a Pinterest board"""

    def __init__(self, data, rest_io):
        """
        Args:
            data (dict): Raw Pinterest API data describing the board
            rest_io (RestIO): reference to the Pinterest REST API
        """
        self._log = logging.getLogger(__name__)
        self._data = data
        self._io = rest_io

    def __str__(self):
        return json.dumps(dict(self._data), sort_keys=True, indent=4)

    def __repr__(self):
        return "<{0} ({1})>".format(self.__class__.__name__, self.name)

    @property
    def unique_id(self):
        """int: The unique identifier associated with this board"""
        return int(self._data['id'])

    @property
    def name(self):
        """str: The name of the board"""
        return self._data['name']

    @property
    def description(self):
        """str: The descriptive text associated with this board"""
        return self._data['description']

    @property
    def url(self):
        """str: Web address for the UI associated with the dashboard"""
        return self._data['url']

    @property
    def num_pins(self):
        """int: The total number of pins linked to this board"""
        return int(self._data['counts']['pins'])

    @property
    def pins(self):
        """Pin: Generator for iterating over the pins linked to this board"""
        self._log.debug('Loading pins for board %s...', self.name)

        properties = {
            "fields": ','.join([
                "id",
                "link",
                "url",
                "creator",
                "board",
                "created_at",
                "note",
                "color",
                "counts",
                "media",
                "attribution",
                "image",
                "metadata",
                "original_link"
            ])
        }

        path = "boards/{0}/pins".format(self.unique_id)
        for cur_page in self._io.get_pages(path, properties):
            assert 'data' in cur_page

            for cur_item in cur_page['data']:
                yield Pin(cur_item, self._io)

    def delete(self):
        """Removes this board and all pins attached to it"""
        self._log.debug('Deleting board %s', repr(self))
        self._io.delete('boards/{0}'.format(self.unique_id))


if __name__ == "__main__":  # pragma: no cover
    pass
