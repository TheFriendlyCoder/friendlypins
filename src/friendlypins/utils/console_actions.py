"""Worker methods used to perform actions performed by fpins console app"""
import logging
import os
from six.moves import urllib
import requests
from tqdm import tqdm
from friendlypins.api import API
from friendlypins.headers import Headers

# Flag used to turn progress bars for downloads and such on and off
DISABLE_PROGRESS_BARS = False

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
        headers = Headers(response.headers)
        log.debug(headers)

        with open(output_file, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)
    except:  # pylint: disable=bare-except
        log.error("Failed to download thumbnail %s", pin.thumbnail.url)
        log.error("See verbose output for details")
        log.debug("Details: ", exc_info=True)
        return 2
    return 0


def download_thumbnails(api_token, board_name, output_folder,):
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
    user = obj.user

    selected_board = None
    for cur_board in user.boards:
        if cur_board.name == board_name:
            selected_board = cur_board
            break
    if not selected_board:
        log.error("Could not find selected board: %s", board_name)
        return 1

    log.info('Downloading thumbnails...')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fmt = "{bar}| {n_fmt}/{total_fmt} [ETA {remaining}]"
    parms = {
        "total": selected_board.num_pins,
        "ncols": 80,
        "bar_format": fmt,
        "disable": DISABLE_PROGRESS_BARS
    }
    retval = 0
    with tqdm(**parms) as pbar:
        for cur_pin in selected_board.pins:
            temp = _download_pin(cur_pin, output_folder)
            if temp:
                retval = temp
            pbar.update()

    return retval

def delete_board(api_token, board_name):
    """Deletes a board owned by a specific user

    :param str api_token: Authentication token for the user who owns the board
    :param str board_name: Name of the board to delete
    :returns: 0 if the board was deleted, otherwise an error code is returned
    :rtype: :class:`int`
    """
    log = logging.getLogger(__name__)
    obj = API(api_token)
    user = obj.user

    selected_board = None
    for cur_board in user.boards:
        if cur_board.name == board_name:
            selected_board = cur_board
            break
    if not selected_board:
        log.error("Could not find selected board: %s", board_name)
        return 1

    log.info(
        "Deleting board %s (%s)",
        selected_board.name,
        selected_board.unique_id)
    selected_board.delete()
    return 0

def create_board(api_token, board_name):
    """Deletes a board owned by a specific user

    :param str api_token: Authentication token for the user who owns the board
    :param str board_name: Name of the board to create
    :returns: 0 if the board was created, otherwise an error code is returned
    :rtype: :class:`int`
    """
    log = logging.getLogger(__name__)
    obj = API(api_token)
    user = obj.user

    result = user.create_board(board_name)

    if result.name != board_name:
        log.error("Unable to create board %s", board_name)
        return 1
    return 0

def check_rate_limit(api_token):
    """Checks to see when the next rate limit renewal is to occur

    :param str api_token: Authentication token for the user who owns the board
    :returns: 0 if the operation succeeded, otherwise an error code
    :rtype: :class:`int`
    """
    log = logging.getLogger(__name__)
    obj = API(api_token)
    log.info("Transactions allowed: %s", obj.transaction_limit)
    log.info("Transactions available: %s", obj.transaction_remaining)
    log.info("Next rate limit renewal is at %s", obj.rate_limit_refresh)
    return 0

if __name__ == "__main__":
    pass
