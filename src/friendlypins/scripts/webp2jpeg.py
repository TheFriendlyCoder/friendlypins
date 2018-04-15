"""Command line tool for converting webp images into jpegs

*WARNING*
This is a prototype, that needs to be more fully tested before it
should be considered production ready.
"""
# pylint: skip-file
import argparse
import logging
import shlex
import sys
import os
from PIL import Image


def _convert(args):
    """Worker function that converts webp images to jpeg

    :param args: Command line arguements customizing the behavior of the action
    :returns: zero on success, non-zero on failure
    :rtype: :class:`int`
    """
    log = logging.getLogger(__name__)
    (output_folder, old_filename) = os.path.split(args.source_file)
    new_filename = os.path.splitext(old_filename)[0] + ".jpeg"
    output_file = os.path.join(output_folder, new_filename)

    if os.path.exists(output_file):
        log.error('Output file already exists %s', output_file)
        return 1

    im = Image.open(args.source_file).convert("RGB")
    im.save(output_file, "jpeg")

    if args.delete:
        os.remove(args.source_file)

    return 0


def get_args(args):
    """Helper method used to parse command line parameters

    :param str args:
        optional command line arguements to be parsed
        if not provided, args will be parsed from the console
    :returns: parsed arguments
    :rtype: :class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Tool for converting webp formatted images to jpeg"
    )

    # Global options
    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=0)
    parser.add_argument(
        "source_file",
        action="store",
    )

    msg = "Deletes original webp source file after conversion completes."
    parser.add_argument(
        '--delete', '-d',
        action="store_true",
        help=msg
    )

    # If we've been given debugging arguments, convert them to the
    # format argparse expects
    if args:
        args = shlex.split(args)

    # By default, if no arguments are given, show online help
    if len(sys.argv) <= 1 and not args:
        args = ["-h"]

    # parse command line args
    return parser.parse_args(args)


def configure_logging(verbosity):
    """Configures the global logger for the application

    :param int verbosity:
        numeric value for the verbosity level for the log
        the larger the number, the more verbose the output
    """
    # Configure a console logger for everything that should show up
    # on the shell to the user
    console_handler = logging.StreamHandler(sys.stdout)
    if verbosity == 0:
        console_handler.setLevel(logging.INFO)
    else:
        console_handler.setLevel(logging.DEBUG)

    # Configure a file logger for all verbose output to be streamed
    # to regardless of the source
    file_handler = logging.FileHandler('webp2jpeg.log', 'w')
    fmt = '%(asctime)s %(levelname)s (%(name)s.%(funcName)s) %(message)s'
    file_formatter = logging.Formatter(fmt=fmt)
    file_handler.setFormatter(file_formatter)


    # Make sure we capture everything with the global logger
    global_log = logging.getLogger()
    global_log.setLevel(logging.DEBUG)

    global_log.addHandler(file_handler)

    # Make sure we hook our console loggers to the appropriate logger
    # based on the level of verbosity the user has requested
    if verbosity < 2:
        log = logging.getLogger('friendlypins')
        log.addHandler(console_handler)
    else:
        global_log.addHandler(console_handler)


def main(args=None):
    """Entry point function

    :params str args:
        sample command line parameters to use when launching the tool
        used for debug and testing purposes only
        When not provided, arguments will be parsed from the command line

    :returns: error code produced by completing the given operation

    :rtype: :class:`int`
    """
    log = logging.getLogger(__name__)
    try:
        parser = get_args(args)
        configure_logging(parser.verbose)
        retval = _convert(parser)
        if retval == 0:
            log.info("Operation completed successfully!")
        return retval
    except Exception:  # pylint: disable=broad-except
        log.error("Critical error processing command")
        log.error("See verbose output for details")
        log.debug("Details: ", exc_info=True)
        return -1

if __name__ == "__main__":
    main("my/path/test.webp")
