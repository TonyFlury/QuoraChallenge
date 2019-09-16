=====================================
Getting Started - Using the Framework
=====================================

The Quora challenge framework is very easy to use and can do 3 main useful things :

    - `Get the challenge Description <description>`_
    - `Automatically test your function <autotest>`_

.. note::
    The quorachallenge framework relies heavily on being able to download data and descriptions from the public internet, so you need to ensure you have a working network connection
    when using the framework.

.. _description:

To get the challenge Description
--------------------------------

To get a description of the challenge (in this case 'challenge1') use the :ref:`describe function<function_describe>`.

.. code-block:: pycon

    >>> import quorachallenge
    >>> quorachallenge.describe('challenge1')

This code snippet will open a new web browser tab or window and display the description of the challenge.


.. _autotest:

Automatically test your function
--------------------------------
To test your function which you think solves a given challenge use the :ref:`AutoTest Decorator<function_AutoTest>`.

Imagine we have written function ``my_func`` to 'solve challenge1'

.. code-block:: python

    import quorachallenge

    @quorachallenge.autotest('challenge')
    def my_func(a, b):
        return a+b

Then this code snippet will automatically test my_func against all of the test cases defined for this challenge, and report any errors or exceptions that occur during the testing.
The displayed messages will identify the test case id that failed and some details of the failure.

The :ref:`AutoTest Decorator<function_AutoTest>` can also be used in a more indirect way as shown in this example

.. code-block:: pycon

    >>> import quorachallenge as qc
            ...
    >>> tester = qc.autotest('challenge1', defer_results=True)
    >>> passed = tester(func)
    >>> passed
    False
    >>> print('\n'.join(tester.errors))
    Test 500 - Incorrect result : Expected (0) != Returned (1)
    >>> tester.results('500')
    'Test 500 - Incorrect result : Expected (0) != Returned (1)'

The :ref:`AutoTest Decorator<function_AutoTest>` can also be passed a specific test id, so as to repeat just that single
test case. This can be very useful in debugging failures.

.. display_testdata:

Display testdata
----------------
To display the test data for a given challenge use the :ref:`testdata function<function_testdata>`.

.. code-block:: pycon

    >>> import quorachallenge
    >>> quorachallenge.testdata('challenge1',test_id='500')
    ------
    Id : 500
    Called as : your_function(0,0)
    Expected to return : 0

This code snippet will display all the test data that exists for 'challenge1'. There is an optional 2nd argument to the
``testdata`` function that allows you to select the test data for just a single test case :

.. code-block:: python

    import quorachallenge

    quorachallenge.testdata('challenge1', '1')

This code snippet will display just the test data for the test case with id '1'; this will be useful if your code is failing one particular test case.

When looking at the test data as displayed from this function :

    Id
        The id of this tests case
    called as
        how the function will be called for this test case
    Raises
        The Exception that the function should raise under this test case
    Returns
        The expected return value for this test case

    For any given test case, there will be either an expected Return value, or an expected Exception listed but not both.
