"""Primary entry point for the Friendly Pinterest library"""

class API(object):  # pylint: disable=too-few-public-methods
    """High level abstraction for the core Pinterest API"""
    def __init__(self):
        self.name = "hello"

    def get_user(self, username=None):
        """Gets all primitives associated with a particular Pinterst user

        :param str username:
            Optional name of a user to look up
            If not provided, the currently authentcated user will be returned
        returns: Pinterest user with the given name
        rtype: :class:`friendly_pinterest.user.User`
        """
        print(self.name)
        if username:
            return None
        return None


if __name__ == "__main__":
    pass
