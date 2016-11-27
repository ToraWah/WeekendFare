"""test_utilities.py

Pytest funcitons for exercising weekendfare.utilities

"""
from os import path, listdir, remove
import configparser
import logging
from datetime import datetime

import pytest
from testfixtures import LogCapture

HERE = path.abspath(path.dirname(__file__))
ROOT = path.dirname(HERE)
ME = __file__.replace(HERE, 'test')
