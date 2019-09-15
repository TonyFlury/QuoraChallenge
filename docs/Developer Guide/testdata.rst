===================
Providing test data
===================

 - :ref:`overview`
 - :ref:`structure`

    - :ref:`keys`

        - :ref:`arguments_detail`
        - :ref:`return_detail`

 - :ref:`examples`

----

.. _overview:

Overiew
-------

As part of providing a challenge, you will provide a set of test cases which aims to confirm that the function provided
meets the requirements of the challenge. The test data should boundary conditions, any exceptional arguments (Empty
strings, None values etc), and of course any argument sets which should cause the function to raise an exception.

.. _structure:

Structure
---------

The testdata.json file is a simple array of dictionaries. If you are not familiar with JSON format it is human readable,
and is very similar to Python formatting :

    - JSON arrays are delimited by square brackets (like Python lists)
    - JSON dictionaries are delimited by braces {like Python dictionaries

 the main relevant differences are that:

    - JSON only uses a double quote character to delimit strings (Python of course can use single or double quotes)
    - Neither JSON lists or dictionaries can have trailing commas (unlike their Python equivalents).

Each dictionary within the JSON array represents a single test case, with it's own call arguments, expected return value
and ability to catch expected exceptions from the function under test. These are provided by a set of keys within the dictionary.

JSON files do not have a format for comments, but if absolutely neccessary, there is nothing to stop you using the
``comment`` key in the dictionary to add notes and comments to each test case. The ``comment`` key is guaranteed to
never be used by the framework, and will be displayed by the :ref:`test_data function<function_testdata>` function

.. _keys:

Dictionary Keys
+++++++++++++++

Within each dictionary, the following keys are considered. All other keys are ignored, and the keys are
case sensitive (all lower case).

    "id" (Optional)
        The unique id for this for test case - either numeric or a string. If not provided, the id is assumed to be the index in the top-level array.
    "arguments" (Mandatory)
        The arguments passed to the function being tested. A string (delimited by single quotes). This is the text that
        appears within the parentheses ( ) as the function is being called - see :ref:`arguments_detail` for more information and examples.
    "return" (Mandatory)
        The return value expected from this function when called with the given arguments. A string delimited by single
        quotes. This is the repr of the return value. - see :ref:`return_detail` for more information and examples. Although
        this value must be present it is ignored if an exception is raised by the function.
    "raises" (Optional)
        The name of the exception that the function should raise given these arguments. A json string delimited by
        single quotes. Can be the name of any exception apart from SyntaxError.

.. _arguments_detail:

Arguments in Detail
~~~~~~~~~~~~~~~~~~~

The value of the ``arguments`` key provides the arguments passed to the function being tested. This value is a string, the
contents of which is the text that appears inside of the parentheses in a normal function call.

For example :

Single Numeric argument
#######################

 .. code-block:: python

            # Actual function call to be executed
            the_function(3)

Equivalent json arguments key :

 .. code-block:: json-object

            "arguments" : "3"

Multiple Numeric Arguments
##########################

 .. code-block:: python

            # Actual function call to be executed
            the_function(5, 7.5)

Equivalent json arguments key :

 .. code-block:: json-object

            "arguments" : "5, 7.5"


String Arguments
################

 .. code-block:: python

            # Actual function call to be executed
            the_function('Hello World')

Equivalent json arguments key :

 .. code-block:: json-object

            "arguments" : "'Hello World'"

Positional and Keyword arguments
################################

 .. code-block:: python

            # Actual function call to be executed
            the_function('Hello World', type='bold')

Equivalent json arguments key :

 .. code-block:: json-object

            "arguments" : "'Hello World', type='bold'"

The ``arguments`` key can be used for any combination of possible positional and keyword arguments, passing
in any builtin type, including strings, lists, tuples, sets, dictionaries, integers, floats and complex values.

.. note::
    It is currently impossible to pass values which derive from a library that needs to be imported. This limitation
    might be removed in a future updated.


.. _return_detail:

Return value in Detail
~~~~~~~~~~~~~~~~~~~~~~

The value of the ``return`` key provides the value which is expected to be returned from the function being tested for
the given arguments value. This value is a string, the contents of which is the repr of the return value.

For example :

Single Numeric return value
###########################

 .. code-block:: python

            the_function( <arguments> ) == 3

Equivalent json return key :

 .. code-block:: json-object

            "return" : "3"

Multiple Numeric return value
#############################

 .. code-block:: python

            the_function( <arguments> ) == (3,15)

Equivalent json return key :

 .. code-block:: json-object

            "return" : "(3, 15)"

or alternatively

 .. code-block:: json-object

            "return" : "3, 15"

String return value
###################

 .. code-block:: python

            # Actual function call to be executed
            the_function( <arguments> ) == 'Hello World'

Equivalent json return key :

 .. code-block:: json-object

            "return" : "'Hello World'"

The ``return`` key can be used for any combination of possible return value of a builtin type, including strings, lists,
tuples, sets, dictionaries, integers, floats and complex values.

.. note::
    It is currently impossible to test for return values which derive from a library that needs to be imported. This limitation
    might be removed in a future updated.


.. _examples:

Examples
--------

The following is a fully set of test data for a the 'example_challenge'. The description is ::

    A function that takes two numbers as postional arguments and adds them together, returning the result.

    The function will take two numbers (integers or floats), and return the two numbers added together, with the
    following reservations :

     - If either value is zero the result returned should be zero
     - If either value is negative the result should be zero
     - If both values are negative the function should raise a ValueError exception.

    There is no requirement for the function to test the type of either argument.

    Exceptions
    ----------

    The Function is required to raise a ValueError exception when both arguments are negative.

The example test data is to confirm that all conditions have been met (at least for the given test data is :

.. code-block:: json

    [
    {"input":"3,5", "return":"8"},
    {"input":"1,2", "return":"3"},
    {"input":"9,11", "return":"20"},
    {"input":"8,7", "return":"15"},
    {"input":"3.5,7.6", "return":"11.1"},
    {"input":"2.3,4.87", "return":"7.17"},
    {"input":"0,1", "return":"0"},
    {"input":"1,0", "return":"0"},
    {"input":"-3,18", "return":"0"},
    {"input":"12,-5", "return":"0"},
    {"input":"-3,-5", "raises":"ValueError"},
    ]


.. note::
    In many cases it would be recommended where possible to write a short script which produces testdata.json file with 100
    or more test cases. An example of an auto generated testdata set is provided in `ExampleTestData`_. The script which
    produced this data is provided as `ExampleTestDataScript`_.

.. _ExampleTestData : https://github.com/TonyFlury/QuoraChallengesTestData/example_challenge/testdata.json
.. _ExampleTestDataScript : https://github.com/TonyFlury/QuoraChallengesTestData/example_challenge/testdata_producer.py

