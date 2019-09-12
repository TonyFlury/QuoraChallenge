#!/usr/bin/env python
# coding=utf-8
"""
# quorachallenge : Quora Challenge Framework

Summary :
    The framework for the Quora development challenges - supporting project description and testing.

Use Case :
    As a entrant in the challenge I want to be able to consistently test the code I enter

Testable Statements :
    ...
"""

from . version import *
import docutils.core
import requests
import pprint
import io

from typing import Union, Any
from collections.abc import Iterable

from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser

def __LoadInDefaultBrowser(html:str) -> None:
    """Display html in the default web browser without creating a temp file.

    Instantiates a trivial http server and calls webbrowser.open with a URL
    to retrieve html from that server.
    """
    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-Type','text/html')
            self.send_header('Content-Length', len(html))
            self.send_header('Content-Encoding','utf-8')
            self.end_headers()
            self.wfile.write(b'<!DOCTYPE html>')
            self.wfile.write(b'<meta charset="utf-8">')
            bufferSize = 1024*1024
            for i in range(0, len(html), bufferSize):
                self.wfile.write(html[i:i+bufferSize])

    server = HTTPServer(('127.0.0.1', 8080), RequestHandler)
    webbrowser.open('http://127.0.0.1:%s' % server.server_port)
    server.handle_request()


def __build_url(challenge_name:str, item:str) -> str:
    return f'https://raw.githubusercontent.com/TonyFlury/QuoraChallengesTestData/master/{challenge_name}/{item}'

def _fetch(challenge_name:str, item:str, optional:bool=False) -> Union[requests.Response, None]:
    """Simple fetch of a resource from a given name and item"

        :param str challenge_name: The name of the challenge to fetch the data for
        :param str item : The item to be fetched
        :param bool optional : Whether the item is optional or not
                               if optional is True then a 404 error generates a None return value
                               if optional is False then a 404 error results in a Value Error
    """
    url = __build_url(challenge_name, item)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.HTTPError:
        if not optional:
            raise ValueError(f"Unable to find description for '{challenge_name}' : Is the name correct ?") from None
        else:
            return None
    except requests.exceptions.RequestException as exc:
        raise exc from None

    return response

def test_data(challenge_name:str, id:str=None):
    """Display the test data for the given challenge

            :param str challenge_name: The case insensitive name for the challenge.
            :param str id: The test id. If left as the default value this function will display the data for all of the test cases.
                           If it is not None, then this function will display the data for the test case with that id - if it exists.

        *The test data is downloaded from a remote site, so this function requires an active public internet connection.*
    """
    challenge_name = challenge_name.lower()

    with io.StringIO() as stream:
        _data = _fetch(challenge_name, item='testdata').json()
        for index, row in enumerate(_data):
            ident = row.get('id', str(index))
            if id is not None and id != ident:
                continue
            row['id'] = ident
            stream.write(f'------\n')
            row['input'] = f'your_function({row["input"]})'
            pprint.pprint(row,stream,indent=4)

        str = stream.getvalue()
    return str

def describe(challenge_name:str, webpage:bool = True):
    """Describe the specified challenge.
        By default this function will open a web-browser and display the description of the challenge.

        :param str challenge_name: The case insensitive name for the challenge.
        :param bool webpage: When True the function will open the users default web browser and display the description in a new tab or windows. When False the function will return the description in `REST`_ format.

        *The description is downloaded from a remote site, so this function requires an active public internet connection.*
    """
    mame = challenge_name.lower()
    response = _fetch(challenge_name, 'description')

    if webpage:
        html = docutils.core.publish_string( source= response.text,  writer_name="html")
        __LoadInDefaultBrowser(html=html)
    else:
        return response

# This decorator is implemented as a class, but uses lowercase naming deliberately
class AutoTest:
    """A callable class/decorator, which will automatically test the function against the challenge requirements.
        By default will immediately report any errors and unexpected exceptions that are raised by the function that is decorated.

        :param str challenge_name: The case insensitive name for the challenge.
        :param str id: A specific id to execute.
        :param bool defer_results: When False the decorator will immediately report test errors and unexpected exceptions upon completion of the automatic testing.
                                   When True the function will be automatically tested but test failures and exceptions are recorded but not automatically reported.

        When defer_results is True, the test failures and exceptions are accessed via the :ref:`errors<property_errors>`
        and :ref:`exceptions<property_exceptions>` properties. and the :ref:`passed property<property_passed>` provides a simple
        True/False report on whether the requested tests completed without errors or unexpected exceptions.

        *The test data for the challenge is downloaded from a remote site, so using this function requires an active public internet connection.*

        Examples :

        As a decorator:
            .. code-block:: python

                @quorachallenge.solves('dummy_challenge')
                def dummy( a, b):
                    return a +b

        Using an explicit instance of the class
            .. code-block:: python

                def dummy( a, b):
                    return a +b

                solver=quorachallenge.solves('dummy_challenge', defer_results=True)
                passed = solver(dummy)

                if not passed:
                    print(solver.errors)
                    print(solver.exceptions)
    """

    def __init__(self, challenge_name:str, id:str = None, defer_results:bool=False):
        """"""
        challenge_name = challenge_name.lower()
        _compare = _fetch(challenge_name, 'compare', optional=True)
        self._data = _fetch(challenge_name, 'testdata').json()
        if _compare:
            _globals = {}
            try:
                exec(_compare.text, __globals = _globals)
            except Exception as e:
                raise e from None

            self._compare = _globals['compare']
        self._name = challenge_name

        self._errors = []
        self._exceptions = []
        self._defer_results = defer_results
        self._id = id
        self._testsrun = False

    def __call__(self, test_function:callable) -> bool:
        """Invoking the decorator will automatically test the function"""
        for index, item in enumerate(self._data):
            id = item.get('id', str(index))
            if self._id is not None and id != self._id:
                continue
            item['id'] = id
            self._compare( index, item, test_function )

        if not self._defer_results:
            print('Exceptions raised:')
            print('\n'.join(self._exceptions))
            print('\n\n')
            print('Test failures : ')
            print('\n'.join(self._errors))

        self._testsrun = True
        return self.passed

    def _compare(self, row_index:0, test_row:dict, test_function:callable) -> None:
        """Execute a comparison for this item in the test data"""
        try:
            id = test_row['id']
            test_input = test_row['input']
            expected_output = test_row['output']

            exceptions = test_row.get('raises', tuple())
            # Convert test names from the json into actual exception types
            can_raise = tuple(__builtins__[name] for name in exceptions if issubclass(__builtins__.get(name, None), Exception))
            expected_output = eval(expected_output)
        except (KeyError, TypeError) as e:
            raise ValueError(f"Invalid test data for challenge '{self._name}' : Id {id}: {e!s}") from None

        try:
            output = eval(f'test_function{test_input}')
        except SyntaxError:
            raise ValueError(f"Invalid test data for challenge '{self._name}' : Id {id}: {e!s}") from None

        except can_raise as e:
            # This is an expected exception for this test case
            return
        except Exception as e:
            self._exceptions.append(f'Unexpected exception raised on Test case id {id} - inputs {test_function.__name__}({test_input}) : Exception raised - {e!s}')
            return

        # compare values
        message = self._compare_values(expected_output, output)

        if message:
            self._errors.append(f'Test {id} - Incorrect result : {message}')

    def _compare_values(self, expected:Any, received:Any):
        """"Intelligent value comparison - with context sensitive messaging"""

        if isinstance(expected, list):
            return self._compare_lists(expected, received)

        if isinstance(expected, dict):
            return self._compare_dicts(expected, received)

        if isinstance(expected,str):
            return self._compare_str(expected,received)

        if isinstance(expected, tuple):
            return self._compare_tuples(expected,received)

        if expected != received:
            return f'Expected {expected} != {received}'

    def _compare_tuple(self, expected:tuple, received:tuple) -> str:
        return self._compare_iterables(expected,received, tuple)

    def _compare_lists(self, expected: list, received:list) -> str:
        return self._compare_iterables( expected,received, list)

    def _compare_str(self, expected: list, received:list) -> str:
        return self._compare_iterables( expected,received, str)

    def _compare_iterables(self, expected : Iterable, received : Iterable, _type:type):
        """Intelligent comparison of iterable - list or str"""
        _type_label = 'list' if _type is list else ('str' if _type is str else 'tuple')

        if not isinstance(received,_type):
            return f'Expected Output should be a {_type_label} - got a {type(received)} entries'

        if len(expected) > len(received):
            return f'Output is too short - expecting {_type_label} of length {len(expected)}, received {_type_label} of length {len(received)}'

        if len(expected) < len(received):
            return f'Output is too long - expecting {_type_label} of length {len(expected)}, received {_type_label} of length {len(received)}'

        for i, (ei, oi) in enumerate(zip(expected, received)):
            res = self._compare_values(ei, oi)
            if res:
                return f'{_type_label} index {i} : {res}'
        return ''

    def _compare_dicts(self, expected : dict, received : dict):
        """Intelligent comparison of dictionaries"""

        if not isinstance(received,dict):
            return f'Expected Output should be a list - got a {type(received)} entries'

        e_keys, o_keys = set(expected.keys()), set(received.keys())

        if e_keys != o_keys:
            missing = e_keys - o_keys
            extra = o_keys - e_keys
            if missing:
                return f'Output is missing these expected keys : {",".join(repr(x) for x in missing)}'
            if extra:
                return f'Output has these extra keys : {",".join(repr(x) for x in extra)}'

        for key in expected:
            if expected[key] != received[key]:
                return f'Value for key {key} is incorrect - expected {expected[key]} but received {received[key]}'

        return ''

    @property
    def errors(self) -> list:
        """The list of errors identified during the automated testing your function"""
        return self._errors

    @property
    def exceptions(self) -> list:
        """The list of unexpected exceptions identified during the automated testing your function"""
        return self._exceptions

    @property
    def passed(self) -> bool:
        """True only if all of the requested tests passed successfully"""
        return self._testsrun and not self.errors and not self.exceptions