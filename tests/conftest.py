import pytest
import sys
from os.path import dirname, abspath

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

@pytest.fixture
def full_choices():
    return {1, 2, 3, 4, 5, 6, 7, 8, 9}