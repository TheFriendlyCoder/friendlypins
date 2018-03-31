import pytest
from friendlypins.api import API

def test_constructor():
    obj = API()

def test_get_user():
    obj = API()
    obj.get_user()

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
