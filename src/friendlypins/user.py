"""Interfaces for interacting with Pinterest users"""
import logging
import json
from friendlypins.board import Board


class User(object):
    """Abstraction around a Pinterest user and their associated data"""

    def __init__(self, url, rest_io):
        """
        Args:
            url (str): URL for this user, relative to the API root
            rest_io (RestIO): reference to the Pinterest REST API
        """
        self._log = logging.getLogger(__name__)
        self._io = rest_io
        self._relative_url = url
        self._data_cache = None

    @staticmethod
    def default_fields():
        """list (str): list of fields we pre-populate when loading user data"""
        return [
            "id",
            "username",
            "first_name",
            "last_name",
            "bio",
            "created_at",
            "counts",
            "image",
            "account_type",
            "url"
        ]

    def refresh(self):
        """Updates cached response data describing the state of this user

        NOTE: This method simply clears the internal cache, and updated
        information will automatically be pulled on demand as additional
        queries are made through the API"""
        self._data_cache = None

    @property
    def _data(self):
        """dict: JSON response containing details of the users' profile

        This internal helper caches the user profile data to minimize the
        number of calls to the REST API, to make more efficient use of rate
        limitations.
        """
        if self._data_cache is not None:
            return self._data_cache
        self._log.debug("Getting authenticated user details...")

        fields = ",".join(self.default_fields())
        temp = self._io.get(self._relative_url, {"fields": fields})
        assert 'data' in temp
        self._data_cache = temp["data"]
        return self._data_cache

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
        self._log.debug('Loading boards for user %s...', self._relative_url)

        properties = {
            "fields": ','.join(Board.default_fields())
        }

        board_url = "{0}/boards".format(self._relative_url)
        for cur_page in self._io.get_pages(board_url, properties):
            assert 'data' in cur_page

            for cur_item in cur_page['data']:
                yield Board.from_json(cur_item, self._io)

    def create_board(self, name, description=None):
        """Creates a new board for the currently authenticated user

        Args:
            name (str): name for the new board
            description (str):  optional descriptive text for the board

        Returns:
            Board: reference to the newly created board
        """
        properties = {
            "fields": ','.join(Board.default_fields())
        }

        data = {"name": name}
        if description:
            data["description"] = description

        result = self._io.post("boards", data, properties)
        return Board.from_json(result['data'], self._io)


if __name__ == "__main__":  # pragma: no cover
    pass
