"""Primitives for operating on Pinterest pins"""
from friendlypins.thumbnail import Thumbnail
from friendlypins.utils.base_object import BaseObject


class Pin(BaseObject):
    """Abstraction around a Pinterest pin"""

    @staticmethod
    def default_url(unique_id):
        """Generates a URL for the REST API endpoint for a pin with a given
        identification number

        Args:
            unique_id (int): unique ID for the pin

        Returns:
            str: URL for the API endpoint
        """
        return "pins/{0}".format(unique_id)

    @staticmethod
    def default_fields():
        """list (str): list of fields we pre-populate when loading pin data"""
        return [
            "id",
            "link",
            "url",
            "board",
            "created_at",
            "note",
            "color",
            "counts",
            "media",
            "attribution",
            "image",
            "metadata",
            "original_link"
        ]

    @property
    def url(self):
        """str: Web address for the UI associated with the pin"""
        return self._data['url']

    @property
    def note(self):
        """str: Descriptive text associated with pin"""
        return self._data['note']

    @property
    def link(self):
        """str: Source URL containing the original data for the pin"""
        return self._data['link']

    @property
    def unique_id(self):
        """int: The unique identifier associated with this pin"""
        return int(self._data['id'])

    @property
    def media_type(self):
        """str: descriptor for the type of data stored in the pin's link

        Returns None if the type of data associated with the Pin
        is unknown
        """
        if 'media' not in self._data:
            return None

        return self._data['media']['type']

    @property
    def thumbnail(self):
        """Thumbnail: the thumbnail image associated with this pin"""
        assert 'image' in self._data
        return Thumbnail(self._data['image'])

    def delete(self):
        """Removes this pin from it's respective board"""
        self._log.debug('Deleting pin %s', self._relative_url)
        self._io.delete(self._relative_url)


if __name__ == "__main__":  # pragma: no cover
    pass
