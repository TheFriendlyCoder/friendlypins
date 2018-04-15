"""Worker methods used to perform actions performed by fpins console app"""
import logging
import os
from six.moves import urllib
import requests
from friendlypins.api import API

def _download_pin(pin, folder):
    """Helper method for downloading a thumbnail from a single pin

    :param pin: reference to the pin to download the thumbnail for
    :type pin: :class:`friendlypins.pin.Pin`
    :param str folder: path where the pin is to be downloaded
    :returns: status code. zero on success, non-zero on error
    :rtype: :class:`int`
    """
    log = logging.getLogger(__name__)
    temp_url = urllib.parse.urlparse(pin.thumbnail.url)
    temp_filename = os.path.basename(temp_url.path)
    output_file = os.path.join(folder, temp_filename)

    if os.path.exists(output_file):
        log.warning(
            "Output file already exists %s. Skipping download.",
            output_file)
        return 0

    try:
        response = requests.get(pin.thumbnail.url, stream=True)
        response.raise_for_status()
        with open(output_file, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)
    except:  # pylint: disable=bare-except
        log.error("Failed to download thumbnail %s", pin.thumbnail.url)
        log.error("See verbose output for details")
        log.debug("Details: ", exc_info=True)
        return 2
    return 0

def download_thumbnails(api_token, board_name, output_folder):
    """Downloads thumbnails of all pins on a board

    :param str api_token: Authentication token for accessing the Pinterest API
    :param str board_name: name of the board containing the pins to process
    :param str output_folder: path where the thumbnails are to be downloaded
    :returns:
        status code describing the result of the action
        zero on success, non-zero on failure
    :rtype: :class:`int`
    """
    log = logging.getLogger(__name__)
    obj = API(api_token)
    user = obj.get_user()

    selected_board = None
    for cur_board in user.boards:
        if cur_board.name == board_name:
            selected_board = cur_board
            break
    if not selected_board:
        log.error("Could not find selected board: %s", board_name)
        return 1

    all_pins = selected_board.all_pins
    log.info('Downloading %s thumbnails...', len(all_pins))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for cur_pin in all_pins:
        retval = _download_pin(cur_pin, output_folder)
        if retval:
            return retval
    return 0

if __name__ == "__main__":
    pass
