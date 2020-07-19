"""Primitives for interacting with Pinterest boards"""
import logging
import json
from friendlypins.pin import Pin


class Board(object):
    """Abstraction around a Pinterest board"""

    def __init__(self, url, rest_io, json_data=None):
        """
        Args:
            url (str): URL for this board, relative to the API root
            rest_io (RestIO): reference to the Pinterest REST API
            json_data (dict):
                Optional JSON response data describing this board
                if not provided, the class will lazy load response data
                when needed
        """
        self._log = logging.getLogger(__name__)
        self._data_cache = json_data
        self._relative_url = url
        self._io = rest_io

    def refresh(self):
        """Updates cached response data describing the state of this board

        NOTE: This method simply clears the internal cache, and updated
        information will automatically be pulled on demand as additional
        queries are made through the API"""
        self._data_cache = None

    @staticmethod
    def default_fields():
        """list (str): list of fields we pre-populate when loading board data"""
        return [
            "id",
            "name",
            "url",
            "description",
            "creator",
            "created_at",
            "counts",
            "image",
            "reason",
            "privacy"
        ]

    @property
    def _data(self):
        """dict: gets response data, either from the internal cache or from the
        REST API"""
        if self._data_cache is not None:
            return self._data_cache
        self._log.debug("Lazy loading board data for: %s", self._relative_url)
        properties = {
            "fields": ','.join(self.default_fields())
        }
        temp = self._io.get(self._relative_url, properties)
        assert "data" in temp
        self._data_cache = temp["data"]

        return self._data_cache

    @classmethod
    def from_json(cls, json_data, rest_io):
        """Factory method that instantiates an instance of this class
        from JSON response data loaded by the caller

        Args:
            json_data (dict):
                pre-loaded response data describing the board
            rest_io (RestIO):
                pre-initialized session object for communicating with the
                REST API

        Returns:
            Board: instance of this class encapsulating the response data
        """
        board_url = "boards/{0}".format(json_data["id"])
        return Board(board_url, rest_io, json_data)

    @property
    def json(self):
        """dict: returns raw json representation of this object"""
        return self._data

    def __str__(self):
        return json.dumps(self._data, sort_keys=True, indent=4)

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
        self._log.debug('Loading pins for board %s...', self._relative_url)

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

        path = "{0}/pins".format(self._relative_url)
        for cur_page in self._io.get_pages(path, properties):
            assert 'data' in cur_page

            for cur_item in cur_page['data']:
                yield Pin(cur_item, self._io)

    def delete(self):
        """Removes this board and all pins attached to it"""
        self._log.debug('Deleting board %s', self._relative_url)
        self._io.delete(self._relative_url)


if __name__ == "__main__":  # pragma: no cover
    pass
