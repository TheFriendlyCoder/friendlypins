"""Interfaces for interacting with Pinterest users"""
import logging
import json
from friendlypins.board import Board


class User(object):
    """Abstraction around a Pinterest user and their associated data"""

    def __init__(self, data, rest_io):
        """
        Args:
            data (dict): JSON data parsed from the API
            rest_io (RestIO): reference to the Pinterest REST API
        """
        self._log = logging.getLogger(__name__)
        self._data = data
        self._io = rest_io

    def __str__(self):
        return json.dumps(dict(self._data), sort_keys=True, indent=4)

    def __repr__(self):
        return "<{0} ({1} {2})>".format(
            self.__class__.__name__,
            self.first_name,
            self.last_name)

    @property
    def unique_id(self):
        """int: Gets the internal unique ID associated with the user"""
        return int(self._data['id'])

    @property
    def first_name(self):
        """str: the first name of the user"""
        return self._data['first_name']

    @property
    def last_name(self):
        """str: the last name of the user"""
        return self._data['last_name']

    @property
    def name(self):
        """str: the full name of the user

        alias for first_name + last_name
        """
        return "{0} {1}".format(self.first_name, self.last_name)

    @property
    def url(self):
        """str: the URL of the users profile"""
        return self._data['url']

    @property
    def num_pins(self):
        """int: the total number of pins owned by this user"""
        return int(self._data['counts']['pins'])

    @property
    def num_boards(self):
        """int: the total number of boards owned by this user"""
        return int(self._data['counts']['boards'])

    @property
    def boards(self):
        """Board: Generator for iterating over the boards owned by this user"""
        self._log.debug('Loading boards for user %s...', self.name)

        properties = {
            "fields": ','.join([
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
            ])
        }

        for cur_page in self._io.get_pages("me/boards", properties):
            assert 'data' in cur_page

            for cur_item in cur_page['data']:
                yield Board(cur_item, self._io)

    def create_board(self, name, description=None):
        """Creates a new board for the currently authenticated user

        Args:
            name (str): name for the new board
            description (str):  optional descriptive text for the board

        Returns:
            Board: reference to the newly created board
        """
        properties = {
            "fields": ','.join([
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
            ])
        }

        data = {"name": name}
        if description:
            data["description"] = description

        result = self._io.post("boards", data, properties)
        return Board(result['data'], self._io)


if __name__ == "__main__":  # pragma: no cover
    pass
