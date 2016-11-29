#Getting Started
WeekendFare is a utility to help users find last-minute flight deals.  Using Google's [QPX Express API](https://developers.google.com/qpx-express/) an attempt at a easy CLI utility.

##For Developers
Quick step-by-step rundown of getting WeekendFare running on your local machine, straight off github.

###Prerequisites
* Python 3.5+
* [QPX API Key](https://developers.google.com/qpx-express/v1/prereqs)
* Packages (see setup steps)
  * [Requests](http://docs.python-requests.org/en/master/)
  * [Plumbum](http://plumbum.readthedocs.io/en/latest/cli.html)
  * [TinyDB](http://tinydb.readthedocs.io/en/latest/)
  * [Dataset](https://dataset.readthedocs.io/en/latest/) ??
  * [JSONschema](http://python-jsonschema.readthedocs.io/en/latest/)
* Should be platform-agnostic, developed on windows 10 x64

###Setting up the project
1. clone (and/or fork) the project
2. set up python3 [Virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) and activate
3. `pip install .` from WeekendFare top-level directory to install prerequisites
  * `pip install -e .` or `pip install .` are preferred to `pip install -r requirements.txt`
4. run `weekendfare/WeekendFare.py` from command line

