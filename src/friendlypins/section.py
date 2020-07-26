"""Primitives for manipulation Pinterest board subsections"""
from friendlypins.utils.base_object import BaseObject
from friendlypins.pin import Pin


class Section(BaseObject):
    """Abstraction around a Pinterest board subsection"""

    @staticmethod
    def default_url(unique_id):
        """Generates a URL for the REST API endpoint for a section with a given identification number

        Args:
            unique_id (int): unique ID for the board

        Returns:
            str: URL for the API endpoint
        """
        return "board/sections/{0}".format(unique_id)

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
        assert isinstance(json_data, str)
        # Example response: <BoardSection 5111575990144913664>
        # we need to extrapolate the section ID from this
        section_id = int(json_data.strip("<").strip(">").split(" ")[-1])
        return cls(cls.default_url(section_id), rest_io)


    @staticmethod
    def default_fields():
        """list (str): list of fields we pre-populate when loading section data"""
        return list()

    @property
    def unique_id(self):
        """int: The unique identifier associated with this board"""
        return int(self._data['id'])

    @property
    def title(self):
        """str: descriptive text associated with this subsection"""
        return self._data["title"]

    @property
    def pins(self):
        """list (Pin): pins associated with this subsection"""
        self._log.debug("Loading pins for board subsection %s...",
                        self._relative_url)
        properties = {
            "fields": ','.join(Pin.default_fields())
        }
        path = "{0}/pins".format(self._relative_url)
        for cur_page in self._io.get_pages(path, properties):
            assert "data" in cur_page

            for cur_item in cur_page["data"]:
                yield Pin.from_json(cur_item, self._io)
