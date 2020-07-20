"""Base class exposing common functionality to all Pinterest primitives"""
import logging
import json


class BaseObject:
    """Common base class providing shared functionality for all Pinterest
    primitives"""

    def __init__(self, url, rest_io, json_data=None):
        """
        Args:
            url (str): URL for this object, relative to the API root
            rest_io (RestIO): reference to the Pinterest REST API
            json_data (dict):
                Optional JSON response data describing this object
                if not provided, the class will lazy load response data
                when needed
        """
        self._log = logging.getLogger(type(self).__module__)
        self._data_cache = json_data
        self._relative_url = url
        self._io = rest_io

    @staticmethod
    def default_fields():
        """Default implementation"""
        raise NotImplementedError(
            "All derived classes must define a default_fields method"
        )

    @staticmethod
    def default_url(unique_id):
        """Default implementation"""
        raise NotImplementedError(
            "All derived classes must define a default_url method"
        )

    def refresh(self):
        """Updates cached response data describing the state of this pin

        NOTE: This method simply clears the internal cache, and updated
        information will automatically be pulled on demand as additional
        queries are made through the API"""
        self._data_cache = None

    @property
    def _data(self):
        """dict: gets response data, either from the internal cache or from the
        REST API"""
        if self._data_cache is not None:
            return self._data_cache
        self._log.debug("Lazy loading data for: %s", self._relative_url)
        properties = {
            "fields": ','.join(self.default_fields())
        }
        temp = self._io.get(self._relative_url, properties)
        assert "data" in temp
        self._data_cache = temp["data"]

        return self._data_cache

    @classmethod
    def from_json(cls, json_data, rest_io):
        """Factory method that instantiates an instance of this class
        from JSON response data loaded by the caller

        Args:
            json_data (dict):
                pre-loaded response data describing the object
            rest_io (RestIO):
                pre-initialized session object for communicating with the
                REST API

        Returns:
            instance of this derived class, pre-initialized with the provided
            response data
        """

        return cls(cls.default_url(json_data["id"]), rest_io, json_data)

    @property
    def json(self):
        """dict: returns raw json representation of this object"""
        return self._data

    def __str__(self):
        return json.dumps(self._data, sort_keys=True, indent=4)

    def __repr__(self):
        return "<{0} ({1}, {2}, {3})>".format(
            self.__class__.__name__,
            self._relative_url,
            self._io,
            self._data_cache
        )
