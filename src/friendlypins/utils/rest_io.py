"""Abstraction around the raw Pinterest REST API calls"""
import logging
import requests
from friendlypins.headers import Headers


class RestIO(object):
    """Interface for low level REST API interactions

    :param str authentication_token:
        Personal API token for authenticating to REST API
    """

    # URL of the root namespace for the Pinterest API
    _root_url = 'https://api.pinterest.com/v1'

    def __init__(self, authentication_token):
        self._log = logging.getLogger(__name__)
        self._token = authentication_token
        self._latest_header = None

    @property
    def root_url(self):
        """Gets root url"""
        return self._root_url

    @property
    def token(self):
        """Gets API token"""
        return self._token

    def get(self, path, properties=None):
        """Gets API data from a given sub-path

        :param str path: sub-path with in the REST API to query
        :param dict properties:
            optional set of request properties to append to the API call
        :returns: json data returned from the API endpoint
        :rtype: :class:`dict`
        """
        self._log.debug(
            "Getting data from %s with options %s",
            path,
            properties
        )
        temp_url = "{0}/{1}".format(self._root_url, path)

        if properties is None:
            properties = dict()
        properties["limit"] = "100"
        properties["access_token"] = self._token

        response = requests.get(temp_url, params=properties)
        response.raise_for_status()

        self._latest_header = Headers(response.headers)
        self._log.debug("%s query header: %s", path, self._latest_header)

        return response.json()

    def delete(self, path):
        """Sends a delete request to a remote endpoint

        :param str path: API endpoint to send delete request to"""
        temp_url = '{0}/{1}'.format(
            self._root_url,
            path)

        properties = {
            "access_token": self._token
        }

        response = requests.delete(temp_url, params=properties)
        response.raise_for_status()
        header = Headers(response.headers)
        self._log.debug("Headers for delete on %s are: %s", path, header)
        self._log.debug("Response from delete was %s", response.text)


if __name__ == "__main__":
    pass
