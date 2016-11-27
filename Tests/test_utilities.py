"""test_utilities.py

Pytest funcitons for exercising weekendfare.utilities

"""
from os import path, listdir, remove
import configparser
import logging
from datetime import datetime

import pytest
from testfixtures import LogCapture

import weekendfare.utilities as wf_utils

HERE = path.abspath(path.dirname(__file__))
ROOT = path.dirname(HERE)
ME = __file__.replace(HERE, 'test')

TEST_BAD_CONFIG_PATH = path.join(HERE, 'bad_config.cfg')
TEST_BAD_PATH = path.join(HERE, 'no_file_here.cfg')
def test_bad_config():
    """failing test: bad parsing"""
    test_config = wf_utils.get_config(TEST_BAD_CONFIG_PATH)

    ## Test keys with bad delimters
    with pytest.raises(KeyError):
        test_config['TEST']['key3']
        test_config['FAILS']['shared_key']

    ## Assert good keys are working as expected
    good_val = test_config['TEST']['key1']
    assert good_val == 'vals'

    ## Test behavior with bad filepath
    with pytest.raises(FileNotFoundError):
        bad_config = wf_utils.read_config(TEST_BAD_PATH)

TEST_GLOBAL_CONFIG_PATH = path.join(HERE, 'test_config_global.cfg')
TEST_LOCAL_CONFIG_PATH = path.join(HERE, 'test_config_local.cfg')
def test_local_filepath_helper():
    """test helper function for fetching local configs"""
    expected_local_filepath = TEST_LOCAL_CONFIG_PATH.replace('.cfg', '_local.cfg')

    assert wf_utils.get_local_config_filepath(TEST_LOCAL_CONFIG_PATH) == TEST_LOCAL_CONFIG_PATH

    assert wf_utils.get_local_config_filepath(TEST_LOCAL_CONFIG_PATH, True) == expected_local_filepath

