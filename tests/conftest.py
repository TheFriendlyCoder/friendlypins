import os
import json
from copy import deepcopy
from pathlib import Path
import pytest
import yaml

CUR_PATH = Path(__file__).parent
DEFAULT_KEY_FILE = CUR_PATH.parent.joinpath("key.txt")
REFERECE_DATA = CUR_PATH.joinpath("reference_data.yaml")


def scrub_response(secret):
    """Helper function that provides a filter function for stripping secrets
    from HTTP responses before they are stored by vcrpy

    Based on the example implementation found her:
    https://vcrpy.readthedocs.io/en/latest/advanced.html#custom-response-filtering

    Example:

        >>> def vcr_config():
        >>>     secret = "1234"
        >>>     return {
        >>>         "before_record_response": scrub_response(secret)
        >>>     }

    Args:
        secret (str): authentication token to be cleaned

    Returns:
        function:
            filter function that can be passed to vcrpy to clean all
            response bodies before they are stored to a cassette
    """
    def inner_scrub_response(response):
        """Inner function used to scrub an HTTP response structure

        Args:
            response (dict):
                data structure describing the contents of the HTTP response

        Returns:
            dict: cleaned version of the response description
        """
        # For running on CI or with local tests only, where we don't need
        # an authentication key, this scrubbing method need not do anything
        if not secret:
            return response

        # Scrub our authentication token from the response body
        # NOTE: for some reason vcrpy expects the response body to be formatted
        #       as a byte array instead of a unicode character string
        body = str(response["body"]["string"])
        if secret in body:
            response["body"]["string"] = \
                body.replace(secret, "DUMMY").encode("utf-8")

        # Scrub our authentication token from the response headers
        if "Location" in response["headers"]:
            # The default location header field has an upper case L
            loc_key = "Location"
        elif "location" in response["headers"]:
            # When the API rate limit has been reached the header field for
            # location gets changes to a lower case l for some weird reason
            loc_key = "location"
        else:
            # Sometimes responses don't have a location field at all in the
            # header. In this case we do nothing
            loc_key = None
        if loc_key:
            temp = response["headers"][loc_key][0]
            response["headers"][loc_key][0] = temp.replace(secret, "DUMMY")

        # One final sanity check to make sure the token doesn't appear
        # anywhere else in the response data structure
        assert secret not in str(response)

        # Return the cleaned response data to the caller
        return response

    # Return our filter function to the caller
    return inner_scrub_response


@pytest.fixture(scope='module')
def vcr_config(request):
    secret = ""
    key_file = request.config.getoption("--key-file")
    if key_file and os.path.exists(key_file):
        with open(key_file) as fh:
            secret = fh.read().strip()
    else:
        # If no auth key provided, let's try and load a default one
        # This is needed when running in an IDE, and to make it easier
        # to run the tests from the shell when one uses a consistent
        # naming convention for the file containing the API key
        if DEFAULT_KEY_FILE.exists():
            secret = DEFAULT_KEY_FILE.read_text().strip()

    retval = {
        "filter_query_parameters": [("access_token", "DUMMY")],
        "before_record_response": scrub_response(secret),
        # Some API responses return a binary-encoded response
        # we decode those before storing in a cassette to make the response
        # data more readable, and to ensure there are no embedded references
        # to our authentication token
        "decode_compressed_response": True,
    }

    # If we don't have an explicit mode set, default to "once"
    # This ensures that we can run tests from within the IDE and
    # have the cassettes auto-generate the first time
    if request.config.getoption("--record-mode") == "none":
        retval["record_mode"] = "once"

    return deepcopy(retval)


@pytest.fixture(scope="function")
def test_env(request):
    if not REFERECE_DATA.exists():
        raise Exception("Reference data for integration tests must be stored in a file name " +
                        str(REFERECE_DATA.name))

    key_file = request.config.getoption("--key-file")
    key = None
    if key_file:
        if not os.path.exists(key_file):
            raise Exception("API authentication token file not found")

        with open(key_file) as fh:
            key = fh.read().strip()
    else:
        # If no explicit auth token can be found, lets try loading a default one
        if DEFAULT_KEY_FILE.exists():
            key = DEFAULT_KEY_FILE.read_text().strip()

    if request.config.getoption("--record-mode") == "rewrite" and not key:
        raise Exception("Rewrite mode can only work with a valid auth key. "
                        "Use --key-file to run the tests.")

    retval = yaml.safe_load(REFERECE_DATA.read_text())
    retval["key"] = key or "DUMMY"  # If we have no auth token, provide a default value

    yield retval


def pytest_collection_modifyitems(config, items):
    """Applies command line customizations to filter tests to be run"""
    if not config.getoption("--skip-functional"):
        return

    skip_functional = pytest.mark.skip(reason="Skipping functional tests")
    for item in items:
        if "test_env" in item.fixturenames:
            item.add_marker(skip_functional)


def pytest_addoption(parser):
    """Customizations for the py.test command line options"""
    parser.addoption(
        "--key-file",
        action="store",
        help="path to file containing PInterest authentication token"
    )
    parser.addoption(
        "--skip-functional",
        action="store_true",
        help="don't run tests that depend on the live Pinterest service"
    )