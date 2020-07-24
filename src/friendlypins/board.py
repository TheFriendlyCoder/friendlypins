"""Primitives for interacting with Pinterest boards"""
from friendlypins.pin import Pin
from friendlypins.utils.base_object import BaseObject


class Board(BaseObject):
    """Abstraction around a Pinterest board"""
    @staticmethod
    def default_url(unique_id):
        """Generates a URL for the REST API endpoint for a board with a given
        identification number

        Args:
            unique_id (int): unique ID for the board

        Returns:
            str: URL for the API endpoint
        """
        return "boards/{0}".format(unique_id)

    @staticmethod
    def default_fields():
        """list (str): list of fields we pre-populate when loading board data"""
        return [
            "id",
            "name",
            "url",
            "description",
            "created_at",
            "counts",
            "image",
            "reason",
            "privacy"
        ]

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
        """pins linked to this board

        Yield:
            Pin:
                generator that lazy loads the definitions for every pin
                on this board
        """
        self._log.debug('Loading pins for board %s...', self._relative_url)

        properties = {
            "fields": ','.join(Pin.default_fields())
        }

        path = "{0}/pins".format(self._relative_url)
        for cur_page in self._io.get_pages(path, properties):
            assert 'data' in cur_page

            for cur_item in cur_page['data']:
                yield Pin.from_json(cur_item, self._io)

    def delete(self):
        """Removes this board and all pins attached to it"""
        self._log.debug('Deleting board %s', self._relative_url)
        self._io.delete(self._relative_url)


if __name__ == "__main__":  # pragma: no cover
    pass
