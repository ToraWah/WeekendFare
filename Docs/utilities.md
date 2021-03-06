#Utility Library
Some general utility functions have been added to make dev life easier.  Please consider importing `weekendfare.utilities` into all WeekendFare libraries

##Config Parsing
WeekendFare uses a static `.cfg` file for hosting all special globals.  To avoid committing secrets (such as API keys), two config files are supported.

1. `weekendfare.cfg`: tracked by git, this is the default/global version of the program's config file
2. `weekendfare_local.cfg`: untracked/.gitignore'd config file.  For use on deployed systems

Loading a config into a program is easy.  See [ConfigParser](https://docs.python.org/3/library/configparser.html) for more info on how to use `config` object.

```python
from os import path

import weekendfare.utilities as wf_utils

HERE = path.abspath(path.dirname(__file__))       #find local directory
CONFIG_FILE = path.join(HERE, 'weekendfare.cfg')  #join() with config filename

config = wf_utils.get_config(CONFIG_FILE)
```

All global scope variables should be loaded from `.cfg` file for easy maintinence.

##Logging
_The road to hell is paved with `print()`_

To best capture the right messages the first time, we strongly encourage using Python's built-in [logging](https://docs.python.org/3/library/logging.html#module-logging) library.  Though debug printing is a developer's best friend, using logging in the first place saves us from needing to rework log messages.

###Getting a logger 
Making loggers for every library is a PITA.  Instead, we offer a common logger with a couple useful tags built in.

```python
from os import path

import weekendfare.utilities as wf_utils

HERE = path.abspath(path.dirname(__file__))       #find local directory
CONFIG_FILE = path.join(HERE, 'weekendfare.cfg')  #join() with config filename

DEBUG = False                                     #flag for debug mode

config = wf_utils.get_config(CONFIG_FILE)
logger = wf_utils.create_logger(
  'demo_logger',
  config=config,            #`LOGGING` level contains logger settings
  log_to_stdout=DEBUG       #enable print-to-screen logging for program debug
)
logger.debug('hello world')
```

`create_logger()` handles all the mess of building the right logger.  Also, it allows easy switching between debug/production modes.

TODO: if project gets bigger than original scope, consider [ProsperCommon](https://github.com/EVEprosper/ProsperCommon) logging utility

###Using a logger
For specifics, refer to the official [logging](https://docs.python.org/3/library/logging.html#module-logging) docs.  Some quick notes for using `logger` in your code:

* `debug`: for verbose output.  Will be turned off in production, but useful for digging into sticky objects and getting more information
* `info`: for status output.  Track the progress of a path through the code.  IE: user input -> request webpage -> saved to datastore -> presented results
* `warning`: non-critical errors.  Troublesome, but non-critical behavior should go into warnings
* `error`: expected/recoverable errors.  `try`/`except` logic will usually have an `error` log
* `critical`: crashing errors.  Unexpected errors, stopping/crashing behavior, unrecoverable issues

NOTE: when logging in a `try`/`except` block, remember to use `exc_info=True` to capture Exception and stacktrace.  Just using `__str__` or `format()` on the exception object does not yield useful logging messages.

```python
test_block = {
  'val1':7,
  'val2':10
}
val_to_find = 'val3'
try:
  val3 = test_block[val_to_find]
except KeyError as err_msg:
  logger.error(
    'EXCEPTION: key not found' +                #error message for humans
    '\r\tval_to_find={0}'.format(val_to_find) + #useful debug info
    '\r\ttest_block={0}'.format(test_block),    
    exc_info=True                               #capture exception/stack trace
  )
  raise err_msg
```

###DEFAULT loggers
So you made a library to be imported as `import weekendfare.demo as demo`.  As a good-programmer, you included `logger` messages throughout the library.  Unfortunately, `demo.py` isn't supposed to be run on its own... so how do you initialize those lovely `logger` calls?

Easy, use a [`NullHandler` logger](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library).  The rule-of-thumb all python libraries should follow are as follows:

1. default/global logger should be a `NullHandler`.  This allows calls to `logging` without actually capturing messages
2. real loggers should be built in `__main__`.  This means only include a real `logger` when the program is run directly
3. libraries should allow importing of `logger` handles, to inherit behavior from the running program

To put another way: only the top-level script should have a real `logger` writing out to file.  All imported libraries should then allow that master-logger to be imported inside to _enable_ logging.  

```python
"""demo.py"""
import logging

logger = logging.getLogger('NULL')        #by default, logger is global, but points to NULL
logger.addHandler(logging.NullHandler())  #separated call because of weird behavior on some systems

def import_logger(logging_obj):
  """works, but not advised"""
  global logger
  logger = logging_obj #overwrite global logger
  
def hello_world():
  logging.info('returning "hello world"')
  return 'hello world
 ```
 
 ```python
 """main.py"""
import weekendfare.utilities as wf_utils
import weekendfare.demo as wf_demo
 
logger = logging.getLogger('NULL')        #very-best-practice, only create logger inside __main__
logger.addHandler(logging.NullHandler())  

if __name__ == '__main__':
  logger = wf_utils.create_logger('demo_logger')  #create logger for main.py
  wf_demo.import_logger(logger)                   #push logger to demo.py
  logger.info('about to call demo.hello_world()')
  hello_response = wf_demo.hello_world()
  logger.info('hello_response={0}'.format(hello_response)
```

Expected log:
```
[INFO:main--<module>--10] about to call demo.hello_world()
[INFO:demo--hello_world--13] returning "hello world"
[INFO:main--<module>--15] hello_response=hello world
```

If `main.py` does not call `wf_demo.import_logger()`, the `[INFO:demo--hello_world--13]` line would not appear.  This is acceptable behavior for an imported library, and favors explicit behavior over implied/assumed behavior.  

##Request Helpers
Fetching stuff from the internet is ezpz with [Requests](http://docs.python-requests.org/en/master/).  In an effort to avoid copy/pasted code, `request` logic has been wrapped up in the utilities package to allow for uniform use.

These have been separated into `fetch_GET_request()` and `fetch_POST_request()` respectively (see [REST API tutorial](http://www.restapitutorial.com/lessons/httpmethods.html) for info on GET/POST).  These should be encapsulated in `try`/`catch` logic, and still return the `request` object for parsing.  Expected behavior should look like this:

```python
import weekendfare.utilities as wf_utils

echo_url = 'https://echo.getpostman.com/post?hello=world'
try:
  req = wf_utils.fetch_GET_request(echo_url)
except Exception as err_msg:
  logger.error(
    'EXCEPTION: request failed!' +
    '\r\turl={0}'.format(echo_url),
    exc_info=True
  )
  raise err_msg
  
webpage_contents = req.json()
webpage_raw = req.text
webpage_headers = req.headers
```

All the error checking is handled inside the helper funciton.  Helper should be able to catch the following issues:

* bad URL
* bad [status code](http://www.restapitutorial.com/httpstatuscodes.html)
* logging progress and errors in URL fetching
* retry flaky connection (TODO)
* tracking API query limits (TODO)

Helper does not cover the following:

* bad JSON (assumes user knows what kind of data they are parsing)
* rotating API keys
* caching responses
* adding header metadata (IE: when query was performed)


