"""test_utilities.py

Pytest funcitons for exercising weekendfare.utilities

"""
from os import path, listdir, remove, makedirs
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
        bad_config = wf_utils.get_config(TEST_BAD_PATH)

TEST_GLOBAL_CONFIG_PATH = path.join(HERE, 'test_config_global.cfg')
TEST_LOCAL_CONFIG_PATH = path.join(HERE, 'test_config_local.cfg')
def test_local_filepath_helper():
    """test helper function for fetching local configs"""
    expected_local_filepath = TEST_LOCAL_CONFIG_PATH.replace('.cfg', '_local.cfg')

    assert wf_utils.get_local_config_filepath(TEST_LOCAL_CONFIG_PATH) == TEST_LOCAL_CONFIG_PATH

    assert wf_utils.get_local_config_filepath(TEST_LOCAL_CONFIG_PATH, True) == expected_local_filepath

#TODO: test local/global key matching
LOG_MESSAGE = 'WeekendFare Logging TEST'
def helper_log_messages(
        logger,
        log_capture_override=None,
):
    """Helper for executing logging same way for every test

    Args:
        logger (:obj:`logging.logger`) logger to commit messages to
        log_capture_override (str): override/filter for testfixtures.LogCapture
        config (:obj: `configparser.ConfigParser`): config override for function values

    Returns:
        (:obj:`testfixtures.LogCapture`) https://pythonhosted.org/testfixtures/logging.html

    """
    with LogCapture(log_capture_override) as log_tracker:
        logger.debug(   LOG_MESSAGE + ' --DEBUG--')
        logger.info(    LOG_MESSAGE + ' --INFO--')
        logger.warning( LOG_MESSAGE + ' --WARNING--')
        logger.error(   LOG_MESSAGE + ' --ERROR--')
        logger.critical(LOG_MESSAGE + ' --CRITICAL--')

    return log_tracker

LOCAL_CONFIG_PATH = path.join(
    ROOT,
    'weekendfare',
    'weekendfare.cfg'
)   #use root config
TEST_CONFIG = wf_utils.get_config(LOCAL_CONFIG_PATH)
LOG_PATH = path.join(HERE, 'logs')
makedirs(LOG_PATH, exist_ok=True) #make sure path is configured for test
def test_cleanup_log_directory(
        logger=None,
):
    """Test0: clean up testing log directory.  Only want log-under-test"""
    if logger:
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    log_list = listdir(LOG_PATH)
    for log_file in log_list:
        if '.log' in log_file:  #mac adds .DS_Store and gets cranky about deleting
            log_abspath = path.join(LOG_PATH, log_file)
            remove(log_abspath)

def test_default_logger(config=TEST_CONFIG):
    """testing basic logger"""
    log_name = 'default'
    logger = wf_utils.create_logger(
        log_name,
        config=config,
        log_path=LOG_PATH
    )

    log_capture = helper_log_messages(logger)
    log_capture.check(
        (log_name, 'INFO',     LOG_MESSAGE + ' --INFO--'),
        (log_name, 'WARNING',  LOG_MESSAGE + ' --WARNING--'),
        (log_name, 'ERROR',    LOG_MESSAGE + ' --ERROR--'),
        (log_name, 'CRITICAL', LOG_MESSAGE + ' --CRITICAL--'),
    )

    test_cleanup_log_directory(logger)

def test_debug_logger(config=TEST_CONFIG):
    """testing debug logger"""
    log_name = 'debug'
    logger = wf_utils.create_logger(
        log_name,
        config=config,
        log_path=LOG_PATH,
        log_to_stdout=True
    )

    log_capture = helper_log_messages(logger)
    log_capture.check(
        (log_name, 'DEBUG',    LOG_MESSAGE + ' --DEBUG--'),
        (log_name, 'INFO',     LOG_MESSAGE + ' --INFO--'),
        (log_name, 'WARNING',  LOG_MESSAGE + ' --WARNING--'),
        (log_name, 'ERROR',    LOG_MESSAGE + ' --ERROR--'),
        (log_name, 'CRITICAL', LOG_MESSAGE + ' --CRITICAL--'),
    )

    test_cleanup_log_directory(logger)
