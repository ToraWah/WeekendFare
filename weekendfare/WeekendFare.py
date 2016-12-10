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

## script globals ##
EARLY_TIME = config.get('WeekendFare', 'early_time')
LATE_TIME = config.get('WeekendFare', 'late_time')

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
    pass

    #from datetime import datetime, timedelta
    #look for strp/strftime.  Parse into datetime object, validate, return processed string


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
        self.kittens = 'calico'
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
        qpx_query['request']['solutions'] = 50  #fixme, make default if not loaded
        qpx_query['request']['refundable'] = 'False' #fixme, make default if not loaded
        logger.debug(json.dumps(qpx_query, indent=2))


if __name__ == '__main__':
    WeekendFare.run()

