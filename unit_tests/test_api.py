import pytest
from friendlypins.api import API

def test_constructor():
    obj = API()

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
