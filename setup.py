"""Wheel setup for WeekendFare Project"""

from os import path, listdir
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

HERE = path.abspath(path.dirname(__file__))

def include_all_subfiles(*args):
    """Slurps up all files in a directory (non recursive) for data_files section

    Note:
        Not recursive, only includes flat files

    Returns:
        (:obj:`list` :obj:`str`) list of all non-directories in a file

    """
    file_list = []
    for path_included in args:
        local_path = path.join(HERE, path_included)

        for file in listdir(local_path):
            file_abspath = path.join(local_path, file)
            if path.isdir(file_abspath):    #do not include sub folders
                continue
            file_list.append(path_included + '/' + file)

    return file_list

class PyTest(TestCommand):
    """PyTest cmdclass hook for test-at-buildtime functionality

    http://doc.pytest.org/en/latest/goodpractices.html#manual-integration

    """
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['test']    #load defaults here

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest_commands = []
        try:    #read commandline
            pytest_commands = shlex.split(self.pytest_args)
        except AttributeError:  #use defaults
            pytest_commands = self.pytest_args
        errno = pytest.main(pytest_commands)
        exit(errno)

setup(
    name='WeekendFare',
    author='TODO',
    author_email='TODO',
    url='https://github.com/ToraWah/WeekendFare',
    download_url='TODO',
    version='0.0.0',
    license='TODO',
    classifiers=[
        'Programming Language :: Python :: 3.5'
    ],
    keywords='QPX flights search',
    packages=find_packages(),
    data_files=[
    #    #TODO: license + README
        ('Tests', include_all_subfiles('Tests')),
        ('Docs', include_all_subfiles('Docs'))
    ],
    package_data={
        'weekendfare':[
            'weekendfare.cfg',
            'qpx_query_template.json'   #TODO: move templates to data_files?
        ]
    },
    install_requires=[
        'requests==2.12.1',
        'tinydb==3.2.1',
        'dataset==0.7.1',
        'plumbum==1.6.2',
        'jsonschema==2.5.1'
    ],
    tests_require=[
        'pytest==3.0.3',
        'testfixtures==4.12.0'
    ],
    cmdclass={
        'test':PyTest
    }
)
