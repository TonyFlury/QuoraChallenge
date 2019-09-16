==================
Framework Details
==================

Overview
--------

The quorachallenge module is a framework to assist developers to are taking part in the Quora Python challenges which will posted ocassionally in  `Python Beginners`_ or `Python Programming`_ `Quora`_ spaces.
The challenges will all require the implementation of a Python function which will meet the specific interface and functionality as required.

The framework provides:
 - immediate access to the description of the challenge
 - the ability to automatically test the function written as an entry to the challenge
 - easy to read test data

Functions
---------

.. _function_describe:

.. autofunction:: quorachallenge.describe

.. _function_testdata:

.. autofunction:: quorachallenge.testdata

autotest class
--------------

.. _function_AutoTest:

.. autoclass:: quorachallenge.autotest

.. _function_results:

.. automethod:: quorachallenge.autotest.results

.. _property_errors:

.. autoproperty:: quorachallenge.autotest.errors

.. _property_exceptions:

.. autoproperty:: quorachallenge.autotest.exceptions

.. _property_passed:

.. autoproperty:: quorachallenge.autotest.passed

.. _property_executed:

.. autoproperty:: quorachallenge.autotest.executed

.. _rst : http://docutils.sourceforge.net/docs/user/rst/quickstart.html
.. _Python Beginners : https://www.quora.com/q/python-beginners
.. _Python Programming : https://www.quora.com/q/python-programming
.. _Quora : https://www.quora.com/