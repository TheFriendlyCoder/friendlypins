"""Package definition for the project"""
import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:  # pragma: no cover
    # If our package isn't currently installed, assume we are running
    # under a development environment and just return a place holder
    __version__ = "0.0.0.dev0"
