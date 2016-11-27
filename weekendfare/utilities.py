"""utilities.py

Helper functions for WeekendFare project

-- Logger
-- Config parser
-- Requests helper

"""
from os import path, makedirs, access, W_OK#, R_OK
import configparser
from configparser import ExtendedInterpolation
import warnings
import logging
from logging.handlers import TimedRotatingFileHandler

HERE = path.abspath(path.dirname(__file__))

DEFAULT_LOGGER = logging.getLogger('NULL')
DEFAULT_LOGGER.addHandler(logging.NullHandler())

def get_config(
        config_filepath,
        local_override=False
):
    """fetch config object for globals

    Args:
        config_filepath (str): path to config file abspath>relpath
        local_override (bool, optional): filepath override for untracked cfg

    Returns:
        (:obj:`configparser.ConfigParser`): config object for later parsing

    """
    config = configparser.ConfigParser(
        interpolation=ExtendedInterpolation(),
        allow_no_value=True,
        delimiters=('='),
        inline_comment_prefixes=('#')
    )

    real_config_filepath = get_local_config_filepath(config_filepath)

    if local_override:  #force lookup tracked config
        real_config_filepath = config_filepath

    with open(real_config_filepath, 'r') as filehandle:
        config.read_file(filehandle)
    return config

def get_local_config_filepath(
        config_filepath,
        force_local=False
):
    """helper for finding local filepath for config

    Args:
        config_filepath (str): path to local config abspath > relpath
        force_local (bool, optional): force return of _local.cfg version

    Returns:
        (str): Path to local config, or global if path DNE

    """
    local_config_filepath = config_filepath.replace('.cfg', '_local.cfg')

    real_config_filepath = ''
    if path.isfile(local_config_filepath) or force_local:
        #if _local.cfg version exists, use it instead
        real_config_filepath = local_config_filepath
    else:
        #else use tracked default
        real_config_filepath = config_filepath

    return real_config_filepath

DEFAULT_LOG_PATH = path.join(path.dirname(HERE), 'logs')
LOG_FORMAT_DEFAULT = '[%(asctime)s;%(levelname)s;%(filename)s;%(funcName)s;%(lineno)s] %(message)s'
LOG_FORMAT_STDOUT = '[%(levelname)s:%(filename)s--%(funcName)s:%(lineno)s] %(message)s'
def create_logger(
        log_name,
        config=configparser.ConfigParser(), #default null ConfigParser
        log_path=DEFAULT_LOG_PATH,
        log_to_stdout=False,
        log_level_override='INFO'
):
    """creates logging handle for easy logging commands

    Args:
        log_name (str): name of logfile
        config_obj (:obj:`configparser.ConfigParser`): config overrides
        log_path (str): path to logfile abspath > relpath
        log_to_stdout (bool, optional): enable std_out logging
        log_level_override (str): log level override setting (for debug printing)

    Returns:
        (:obj:`logging.logger`): logging object for print() replacement

    """
    try:
        logging_cfg = config.get('LOGGING')
    except KeyError:
        logging_cfg = {}
    log_level = logging_cfg.get('log_level', log_level_override)
    log_path  = logging_cfg.get('log_path', log_path)
    log_freq  = logging_cfg.get('log_freq', 'midnight')
    log_total = int(logging_cfg.get('log_total', 30))

    logger = logging.getLogger(log_name)
    log_path = test_logpath(log_path)
    log_filename = log_name + '.log'
    log_abspath = path.join(log_path, log_filename)
    general_handler = TimedRotatingFileHandler(
        log_abspath,
        when=log_freq,
        interval=1,
        backupCount=int(log_total)
    )
    general_formatter = logging.Formatter(LOG_FORMAT_DEFAULT)
    general_handler.setFormatter(general_formatter)
    logger.setLevel(log_level)
    logger.addHandler(general_handler)

    if log_to_stdout:
        #Replaces print() functionality
        logger.setLevel(logging.getLevelName('DEBUG'))
        debug_formatter = logging.Formatter(LOG_FORMAT_STDOUT)
        debug_handler = logging.StreamHandler()
        debug_handler.setFormatter(debug_formatter)
        debug_handler.setLevel(logging.getLevelName('DEBUG'))

        logger.addHandler(debug_handler)

    return logger

def test_logpath(log_path, debug_mode=False):
    """Tests if logger has access to given path and sets up directories

    Note:
        Should always yield a valid path.  May default to script directory
        Will throw warnings.ResourceWarning if permissions do not allow file write at path

    Args:
        log_path (str): path to desired logfile.  Abspath > relpath
        debug_mode (bool): way to make debug easier by forcing path to local

    Returns:
        str: path to log

        if path exists or can be created, will return log_path
        else returns '.' as "local path only" response

    """
    if debug_mode:
        return '.' #if debug, do not deploy to production paths

    ## Try to create path to log ##
    if not path.exists(log_path):
        try:
            makedirs(log_path, exist_ok=True)
        except PermissionError as err_permission:
            #UNABLE TO CREATE LOG PATH
            warning_msg = (
                'Unable to create logging path.  Defaulting to \'.\'' +
                'log_path={0}'.format(log_path) +
                'exception={0}'.format(err_permission)
            )
            warnings.warn(
                warning_msg,
                ResourceWarning
            )
            return '.'
        except Exception as err_msg:
            raise err_msg

    ## Make sure logger can write to path ##
    if not access(log_path, W_OK):
        #UNABLE TO WRITE TO LOG PATH
        warning_msg = (
            'Lacking write permissions to path.  Defaulting to \'.\'' +
            'log_path={0}'.format(log_path) +
            'exception={0}'.format(err_permission)
        )
        warnings.warn(
            warning_msg,
            ResourceWarning
        )
        return '.'
        #TODO: windows behavior requires abspath to existing file

    return log_path
