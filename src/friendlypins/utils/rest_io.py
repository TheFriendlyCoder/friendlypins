"""Abstraction around the raw Pinterest REST API calls"""
import logging
import requests
from friendlypins.headers import Headers
from friendlypins.exceptions import RateLimitException


class RestIO(object):
    """Interface for low level REST API interactions"""

    # URL of the root namespace for the Pinterest API
    _root_url = 'https://api.pinterest.com/v1'

    def __init__(self, authentication_token):
        """
        Args:
            authentication_token (str):
                Personal API token for authenticating to REST API
        """
        self._log = logging.getLogger(__name__)
        self._token = authentication_token
        self._latest_header = None

    @property
    def root_url(self):
        """str: canonical url for the REST API"""
        return self._root_url

    @property
    def token(self):
        """str: authentication token"""
        return self._token

    @property
    def headers(self):
        """Headers: the HTTP headers from the most recent API operation"""
        if not self._latest_header:
            temp_url = "{0}/me".format(self._root_url)
            properties = {"access_token": self._token}
            response = requests.get(temp_url, params=properties)
            self._latest_header = Headers(response.headers)
            self._raise_for_status(response)
        return self._latest_header

    @staticmethod
    def _raise_for_status(response):
        """Helper method that checks for various errors and raises more user
        friendly exceptions for the caller to consume

        Args:
            response (requests.Response):
                response object returned from the HTTP REST API
        """
        if response.status_code == requests.codes.too_many_requests:
            raise RateLimitException(response)

        response.raise_for_status()

    def get(self, path, properties=None):
        """Gets API data from a given sub-path

        Args:
            path (str): sub-path with in the REST API to query
            properties (dict):
                optional set of request properties to append to the API call

        Returns:
            dict: json data returned from the API endpoint
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

        self._log.debug("Get response text is %s", response.text)
        self._latest_header = Headers(response.headers)
        self._log.debug("%s query header: %s", path, self._latest_header)
        self._raise_for_status(response)

        return response.json()

    def post(self, path, data, properties=None):
        """Posts API data to a given sub-path

        Args:
            path (str): sub-path with in the REST API to send data to
            data (str): form data to be posted to the API endpoint
            properties (dict):
                optional set of request properties to append to the API call

        Returns:
            dict: json data returned from the API endpoint
        """
        self._log.debug(
            "Posting data from %s with options %s",
            path,
            properties
        )
        temp_url = "{0}/{1}/".format(self._root_url, path)

        if properties is None:
            properties = dict()
        properties["access_token"] = self._token

        response = requests.post(temp_url, data=data, params=properties)
        self._latest_header = Headers(response.headers)
        self._log.debug("%s query header: %s", path, self._latest_header)
        self._log.debug("Post response text is %s", response.text)

        self._raise_for_status(response)

        return response.json()

    def get_pages(self, path, properties=None):
        """Generator for iterating over paged results returned from API

        Args:
            path (str): sub-path with in the REST API to query
            properties (dict):
                optional set of request properties to append to the API call

        Returns:
            dict: json data returned from the API endpoint
        """
        page = 0
        while True:
            self._log.debug("Loading results page %s", page)
            result = self.get(path, properties)
            yield result

            if "page" not in result:
                break
            if "cursor" not in result["page"]:
                break
            if not result["page"]["cursor"]:
                break

            if properties is None:
                properties = dict()
            properties["cursor"] = result["page"]["cursor"]
            page += 1

    def delete(self, path):
        """Sends a delete request to a remote endpoint

        Args:
            path (str): API endpoint to send delete request to
        """
        temp_url = '{0}/{1}'.format(
            self._root_url,
            path)

        properties = {
            "access_token": self._token
        }

        response = requests.delete(temp_url, params=properties)
        header = Headers(response.headers)
        self._log.debug("Headers for delete on %s are: %s", path, header)
        self._log.debug("Response from delete was %s", response.text)
        self._raise_for_status(response)


if __name__ == "__main__":  # pragma: no cover
    pass
