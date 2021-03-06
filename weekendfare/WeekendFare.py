"""WeekendFare.py

A CLI utility for checking last-minute prices on flights.

"""

from datetime import datetime, timedelta
from os import path
import logging
import json

from plumbum import cli
from tinydb import TinyDB, Query
import dataset
from jsonschema import validate

import weekendfare.utilities as wf_utils

HERE = path.abspath(path.dirname(__file__))
ME = __file__.replace('.py', '')
CONFIG_ABSPATH = path.join(HERE, 'weekendfare.cfg')
config = wf_utils.get_config(CONFIG_ABSPATH)

## Null logger because `cli.Application` will trigger log setup
## Leaving NullHandler will make testing easier later "trust me" (tm)
logger = logging.getLogger(ME).addHandler(logging.NullHandler())

DEBUG = False
## script globals ##
EARLY_TIME = config.get('WeekendFare', 'early_time')
LATE_TIME = config.get('WeekendFare', 'late_time')
REFUND = config.get('WeekendFare', 'refund')
SOLUTIONS = config.get('WeekendFare','solutions')


def build_logger(verbose=False):
    """build and attach logger for regular running

    Args:
        verbose (bool, optional): toggle verbose/stdout logging

    Returns:
        (:obj:`logging.logger`): updates global logger and returns object
    """
    #FIXME: using `global` isn't really the best
    global logger
    logger = wf_utils.create_logger(
        ME,
        config=config,
        log_to_stdout=verbose
        #TODO: log_level_override?
    )
    return logger

def validate_airport(airport_abrev):
    pass

    #if valid:
    #   return airport_abrev
    #else:
    #   raise TypeError('message')

def validate_datetime(datetime_str):
    try:
        datetime.strptime(datetime_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    pass
    """if datetime_str == datetime.strptime():
        return self.date
    else:
        return "Bad date" """
    #from datetime import datetime, timedelta
    #look for strp/strftime.  Parse into datetime object, validate, return processed string

def build_request(request_parameters):
    """function to build QPX request

    Args:
        request_parameters (:obj:`dict`): container with all the magic values in it

    Returns:
        (str): stringified request_parameters to match QPX template (https://qpx-express-demo.itasoftware.com/)

    """
    pass

    #TOOLS: json.dumps(data, indent=2) https://docs.python.org/3.5/library/json.html
    # Extra credit: validate against qpx_query_template with jsonschema (advanced)

def parse_response(
        response_data,
        price_filter=None,
        #additional search criteria here
        #don't worry, it can be ugly for now
    ):
    """function to parse the response object for important info

    Args:
        (:obj:`dict` json): data from QPX

    Returns:
        (:obj:`dict`) flights worth knowing about

    """
    pass

QPX_CACHE = path.join(HERE, config.get('WeekendFare', 'qpx_cache'))
QPX_DB = TinyDB(QPX_CACHE)
def try_cache(
        qpx_query_slice,
        qpx_query_filters=None
):
    """check the tinyDB cache for value

    Note: only checks first slice (single slice tester)

    Args:
        (:obj:`dict`): qpx_query_slice

    Returns:
        (:obj:`dict` or None): value in tinydb

    """
    c_query = Query()

    record = QPX_DB.search(
        c_query.origin == qpx_query_slice['origin'] & \
        c_query.destination == qpx_query_slice['destination'] & \
        c_query.date == qpx_query_slice['date']
    )

    #TODO: add qpx_query_filters for better offline/cache behavior

    if record:
        logger.debug('--record found')
        logger.debug(record)
        return record

    else:
        return None


def fetch_query(
        qpx_query,
        debug=DEBUG
):
    """Fetch data from qpx and return in normal format

    Args:
        (:obj:`dict` json): QPX-validated query for fetching
        (bool, optional): debug mode: run in headless mode

    Returns:
        (:obj:`dict`): QPX response (or cached version)

    """
    pass

class WeekendFare(cli.Application):
    """Plumbum CLI application: WeekendFare"""
    # http://plumbum.readthedocs.io/en/latest/cli.html
    debug = cli.Flag(
        ['d', '--debug'],
        help='Debug mode, send data to local files'
    )
    #TODO: debug mode:
    # -- use local results if possible
    # -- force user acceptance for hitting API
    # -- drop debug files
    # -- toggle global DEBUG option?

    verbose = cli.Flag(
        ['-v', '--verbose'],
        help='enable verbose logging'
    )

    #TODO: add query @cli.switch() calls

    # -- times to fly between (optional)

    # -- pasengers (all fields required)
    pas_adult = cli.CountOf(["-a", "--adult"], help = "Adult ticket")
    pas_child = cli.CountOf(["-c", "--child"], help = "Child ticket")
    pas_infant_lap = cli.CountOf(["-l", "--lap"], help = "Infant riding in lap")
    pas_infant_seat = cli.CountOf(["-i", "--infant"], help = "Infant riding in seat")
    pas_senior = cli.CountOf(["-s", "--senior"], help = "Senior ticket")
    # -- airline (optional)
    # -- round-trip?
    def roundtrip(home):
        if True:
            return_date = "2016-12-11"
            early_return_time = "06:00"
            late_return_time = "22:00"
        else:
            return
    # -- direct flight
    nonstop = cli.Flag(
        ["-n", "--nonstop"],
        help='Nonstop flight',
    )
    layover_wait = 60
    # -- refundable? (cli.Flag)
    refund = cli.Flag(
        ['-r', '--refund'],
        help='If tickets need to be refundable'
    )

    #TODO: tryhard mode: multiple "slices"
    # Use either of the following:
    # -- repeatable switches: http://plumbum.readthedocs.io/en/latest/cli.html#repeatable-switches
    # -- sub commands? http://plumbum.readthedocs.io/en/latest/cli.html#sub-commands

    def main(self):
        """CLI `main`.  Runs core logic of application"""
        global DEBUG
        if self.debug:
            DEBUG = self.debug
        build_logger(self.verbose)
        logger.debug('hello world')
        # -- start city
        start = cli.terminal.readline("Origin Airport code:") #make sure is 3-digit str()
        start.replace('\n', '')
        start = validate_airport(start)
        # -- destination city
        dest = cli.terminal.readline("End Airport code:") #make sure is 3-digit  str()
        dest.replace('\n', '')
        dest = validate_airport(dest)
        # -- travel date(s)
        date = cli.terminal.readline("Day of flight (YYYY-MM-DD):")
        date.replace('\n', '')
        date = validate_datetime(date)


        qpx_query = {}
        qpx_query['request'] = {}
        qpx_query['request']['slice'] = [] #[slice1, slice2, slice3]
        slice_data = {
            'origin': start,
            'destination': dest,
            'date': date
        }
        qpx_query['request']['slice'].append(slice_data)
        qpx_query['request']['pasengers'] = {
            'adultCount': self.pas_adult,
            'infantInLapCount': self.pas_infant_lap,
            'incantInSeatCount': self.pas_infant_seat,
            'childCount': self.pas_child,
            'seniorCount': self.pas_senior
        }
        qpx_query['request']['solutions'] = SOLUTIONS #fixme, make default if not loaded
        qpx_query['request']['refundable'] = REFUND #fixme, make default if not loaded
        logger.debug(json.dumps(qpx_query, indent=2))


if __name__ == '__main__':
    WeekendFare.run()

