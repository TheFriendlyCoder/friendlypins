"""Primary entry point for the Friendly Pinterest library"""
import logging
from friendlypins.user import User
from friendlypins.board import Board
from friendlypins.pin import Pin
from friendlypins.utils.rest_io import RestIO


class API(object):
    """High level abstraction for the core Pinterest API"""

    def __init__(self, personal_access_token):
        """
        Args:
            personal_access_token (str):
                API authentication token used for secure access to a users'
                Pinterest data
        """
        self._log = logging.getLogger(__name__)
        self._io = RestIO(personal_access_token)

    def get_board_by_id(self, board_id):
        """Locates a specific Pinterest board given it's internal identifier

        NOTE: this API assumes that the ID provided references a valid board.
        If it does not, the object returned will be invalid and any attempts
        to access data from the board will result in an error.

        Args:
            board_id (int):
                the unique identifier for the board

        Returns:
            Board: reference to the Pinterest board
        """
        board_url = "boards/{0}".format(board_id)
        return Board(board_url, self._io)

    def get_pin_by_id(self, pin_id):
        """Locates a specific Pinterest pin given it's internal identifier

        NOTE: this API assumes that the ID provided references a valid pin.
        If it does not, the object returned will be invalid and any attempts
        to access data from the pin will result in an error.

        Args:
            pin_id (int):
                the unique identifier for the board

        Returns:
            Pin: reference to the Pinterest pin
        """
        pin_url = "pins/{0}".format(pin_id)
        return Pin(pin_url, self._io)

    @property
    def user(self):
        """User: Gets all primitives associated with the authenticated user"""
        return User("me", self._io)

    @property
    def rate_limit_refresh(self):
        """datetime.datetime: Gets the time when the next refresh for API
        queries takes effect"""
        return self._io.headers.time_to_refresh

    @property
    def transaction_limit(self):
        """int: Gets the total number of transactions per hour we're allotted
        """
        return self._io.headers.rate_limit

    @property
    def transaction_remaining(self):
        """int: Gets the total number of transactions per hour we're allotted
        """
        return self._io.headers.rate_remaining


if __name__ == "__main__":  # pragma: no cover
    pass
