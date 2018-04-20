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

    @property
    def headers(self):
        """Gets the HTTP headers from the most recent API operation

        :rtype: :class:`friendlypins.headers.Headers`
        """
        return self._latest_header

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

        self._log.debug("Get response text is %s", response.text)
        self._latest_header = Headers(response.headers)
        self._log.debug("%s query header: %s", path, self._latest_header)
        response.raise_for_status()

        return response.json()

    def post(self, path, data, properties=None):
        """Posts API data to a given sub-path

        :param str path: sub-path with in the REST API to send data to
        :param dict data: form data to be posted to the API endpoint
        :param dict properties:
            optional set of request properties to append to the API call
        :returns: json data returned from the API endpoint
        :rtype: :class:`dict`
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

        response.raise_for_status()

        return response.json()

    def get_pages(self, path, properties=None):
        """Generator for iterating over paged results returned from API

        :param str path: sub-path with in the REST API to query
        :param dict properties:
            optional set of request properties to append to the API call
        :returns: json data returned from the API endpoint
        :rtype: Generator of :class:`dict`
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

        :param str path: API endpoint to send delete request to"""
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
        response.raise_for_status()

if __name__ == "__main__":
    pass
