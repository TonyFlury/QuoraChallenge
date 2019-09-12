#!/usr/bin/env python
# coding=utf-8
"""
# quorachallenge : Quora Challenge Framework

Summary :
    The framework for the Quora development challenges - supporting project description and testing.
Use Case :
    As a entrant in the challenge I want to be able to consitently test the code I enter

Testable Statements :
    ...
"""
import inspect
import re
import unittest
import re
import click
import sys
import quorachallenge as qc
import requests

from unittest.mock import Mock, patch

def patched_requests(status=200,test_data=None, compare=None,description=''):

    def build_response( arg ):
        response = Mock(name='response')

        if status == 404:
            response.raise_for_status = Mock(side_effect=requests.HTTPError)
            return response

        if not compare and 'compare' in arg:
            response.raise_for_status = Mock(side_effect=requests.HTTPError)
            return response

        if compare and 'compare' in arg:
            response.text = compare
            response.raise_for_status.return_value = None
            return response

        if 'testdata' in arg:
            response.json.return_value = test_data
            response.raise_for_status.return_value = None
            return response

        if 'description' in arg:
            response.text = description
            response.raise_for_status.return_value = None
            return response

    get = Mock(name = 'requests.get')
    get.side_effect = build_response

    return get

class OrderedTestSuite(unittest.TestSuite):
    def __iter__(self):
        return iter(sorted(self._tests, key=lambda x:str(x)))

class TestCases(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(1,2)','output':'3'}],description='This is the description'))
    def test_000_010_single_pass(self):
        """Test a simple function which will pass once"""

        def func(a,b):
            return a + b

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)

        solver(func)
        self.assertTrue(solver.passed)

    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(1,2)','output':'3'},
                                                                      {'input':'(5,3)','output':'8'}],
                                                                        description='This is the description'))
    def test_000_020_multiple_pass(self):
        """Ensure that the multiple correct passes are recorded"""

        def func(a,b):
            return a + b

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)

        solver(func)
        self.assertTrue(solver.passed)
        self.assertEqual(len(solver.errors), 0)
        self.assertEqual(len(solver.exceptions), 0)


    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(1,2)','output':'3'},
                                                                      {'input':'(5,3)','output':'7'}],description='This is the description'))
    def test_000_100_single_fail(self):
        """Single test cases with a single test failure"""
        def func(a,b):
            return a + b

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)

        solver(func)
        self.assertFalse(solver.passed)
        self.assertEqual(len(solver.errors), 1)
        self.assertEqual(len(solver.exceptions), 0)

    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(1,2)','output':'4'},
                                                                      {'input':'(5,3)','output':'7'}],description='This is the description'))
    def test_000_110_multiple_fail(self):
        """Multiple test failures"""

        def func(a,b):
            return a + b

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)

        solver(func)
        self.assertFalse(solver.passed)
        self.assertEqual(len(solver.errors), 2)
        self.assertEqual(len(solver.exceptions), 0)

    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(1,2)','output':'3'},{'input':'(5,3)','output':'8'}],description='This is the description'))
    def test_000_200_exceptions(self):
        """Function under tests raises an exception"""
        def func(a,b):
            if a == 1 or b == 1:
                raise AttributeError
            return a + b

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)

        passed = solver(func)
        self.assertFalse(solver.passed)
        self.assertEqual(len(solver.exceptions), 1)
        self.assertEqual(len(solver.errors), 0)

    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(1)', 'raises':['ValueError'], 'output':'3'},{'input':'(3)','output':'9'}],description='This is the description'))
    def test_000_210_allowed_exceptions(self):
        """Function under tests raises an exception"""
        def func(a):
            if a == 1:
                raise ValueError
            return a*3

        solver = qc.AutoTest(challenge_name ='challenge1', id='0', defer_results=True)

        passed = solver(func)
        self.assertTrue(solver.passed)
        self.assertEqual(len(solver.exceptions), 0)
        self.assertEqual(len(solver.errors), 0)

    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(3)','output':'[1,2]'},{'input':'(4)','output':'[1,2,3]'}],description='This is the description'))
    def test_100_000_list_correct(self):
        """Received list is too short - expect a useful error."""

        def func(a):
            return list(range(1,a))

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)

        passed = solver(func)
        self.assertTrue(passed)

    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(3)','output':'[1,2,3]'},{'input':'(4)','output':'[1,2,3,4]'}],description='This is the description'))
    def test_100_010_list_too_short(self):
        """Received list is too short - expect a useful error."""

        def func(a):
            return list(range(1,a))

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)

        passed = solver(func)
        self.assertRegex(solver.errors[0], r'Test 0 - Incorrect result : Output is too short - expecting list of length 3, received list of length 2')
        self.assertRegex(solver.errors[1], r'Test 1 - Incorrect result : Output is too short - expecting list of length 4, received list of length 3')

    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(3)','output':'[1,2,3]'},{'input':'(4)','output':'[1,2,3,4]'}],description='This is the description'))
    def test_100_020_list_too_long(self):
        """Received list is too long - expect a useful error."""

        def func(a):
            return list(range(1,a*2))

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)

        passed = solver(func)
        self.assertRegex(solver.errors[0], r'Test 0 - Incorrect result : Output is too long - expecting list of length 3, received list of length 5')
        self.assertRegex(solver.errors[1], r'Test 1 - Incorrect result : Output is too long - expecting list of length 4, received list of length 7')

    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(3)','output':'[1,2,4]'},{'input':'(4)','output':'[2,2,3,4]'}],description='This is the description'))
    def test_100_030_list_incorrect(self):
        """Returned result is the correct length but is incorrect at a particular position"""
        def func(a):
            return list(range(1,a+1))

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)

        passed = solver(func)

        self.assertRegex(solver.errors[0], r'Test 0 - Incorrect result : list index 2 : Expected 4 != 3')
        self.assertRegex(solver.errors[1], r'Test 1 - Incorrect result : list index 0 : Expected 2 != 1')

    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(3)','output':'{1:1,2:2}'},
                                                                      {'input':'(4)','output':'{1:1,2:2,3:3}'}],
                                                      description='This is the description'))
    def test_200_000_dict_correct(self):
        """Returned result is a correct dictionary"""
        def func(a):
            return {x:x for x in range(1, a)}

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)

        passed = solver(func)
        self.assertTrue(passed)


    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(3)','output':'{1:1,2:2}'},
                                                                      {'input':'(4)','output':'{1:1,2:2,3:3}'}],
                                                      description='This is the description'))
    def test_200_010_dict_missing_key(self):
        """Returned result is dictionary with missing keys"""
        def func(a):
            return {x:x for x in range(1, int(a/2)-1)}

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)
        passed = solver(func)


        self.assertFalse(passed)
        self.assertEqual(len(solver.errors),2)
        self.assertRegex(solver.errors[0], r'Test 0 - Incorrect result : Output is missing these expected keys : 1,2')
        self.assertRegex(solver.errors[1], r'Test 1 - Incorrect result : Output is missing these expected keys : 1,2,3')

    @patch.object(qc.requests,'get', patched_requests(200, test_data=[{'input':'(1)','output':'{1:1}'},
                                                                      {'input':'(2)','output':'{1:1,2:2}'}],
                                                      description='This is the description'))
    def test_200_020_dict_extra_key(self):
        """Returned result is dictionary with extra keys"""
        def func(a):
            return {x:x for x in range(1, (a*2)+1)}

        solver = qc.AutoTest(challenge_name ='challenge1', defer_results=True)
        passed = solver(func)

        self.assertFalse(passed)

        self.assertEqual(len(solver.errors),2)
        self.assertRegex(solver.errors[0], r'Test 0 - Incorrect result : Output has these extra keys : 2')
        self.assertRegex(solver.errors[1], r'Test 1 - Incorrect result : Output has these extra keys : 3,4')

# noinspection PyMissingOrEmptyDocstring,PyUnusedLocal
def load_tests(loader, tests=None, patterns=None,excludes=None):
    """Load tests from all of the relevant classes, and order them"""
    classes = [cls for name, cls in
               inspect.getmembers(sys.modules[__name__],inspect.isclass)
               if issubclass(cls, unittest.TestCase)]

    suite = OrderedTestSuite()
    for test_class in classes:
        tests = loader.loadTestsFromTestCase(test_class)
        if patterns:
            tests = [test for test in tests if all(re.search(pattern, test.id()) for pattern in patterns)]
        if excludes:
            tests = [test for test in tests if not any(re.search(exclude_pattern,test.id()) for exclude_pattern in excludes)]
        suite.addTests(tests)
    return suite

@click.command()
@click.option('-v', '--verbose', default=2, help='Level of output', count=True)
@click.option('-s', '--silent', is_flag=True, default=False, help='Supress all output apart from a summary line of dots and test count')
@click.option('-x', '--exclude', metavar='EXCLUDE', multiple=True, help='Exclude where the names contain the [EXCLUDE] pattern')
@click.argument('patterns', nargs=-1, required=False, type=str)
def main(verbose, silent, patterns, exclude):
    """Execute the unit test cases where the test id match the patterns

    Test cases are only included for execution if their names (the class name and the method name)
    contain any of the text in any of the [PATTERNS].
    Test cases are excluded from execution if their names contain any of the text in any of the [EXCLUSION]
    patterns

    Both [PATTERNS] and [EXCLUSION] can be regular expressions (using the re syntax)

    \b
    A single -v produces a single '.' for each test executed
    Using -v -v produces an output of the method name and 1st line of any
            doc string for each test executed
    """
    verbose = 0 if silent else verbose

    ldr = unittest.TestLoader()
    test_suite = load_tests(ldr, patterns=patterns, excludes=exclude)
    unittest.TextTestRunner(verbosity=verbose).run(test_suite)

if __name__ == '__main__':
    main()