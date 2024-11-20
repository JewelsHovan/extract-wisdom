import pytest
import os

def pytest_configure(config):
    """Create test directories if they don't exist"""
    test_dir = os.path.dirname(__file__)
    data_dir = os.path.join(test_dir, "data")
    output_dir = os.path.join(test_dir, "output")
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
