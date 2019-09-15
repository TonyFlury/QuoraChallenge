=================================
Providing a challenge Description
=================================

The description file must be a clear and unambiguous description of the challenge, written in `rST`_ format,

It is strongly recommended that :

 - The challenge should have a clear title
 - The remainder of the description should be structured as a Python docstring [#docstringFormat]_.

   Specifically that is :

    - Following the title, a one sentence summary of challenge.
    - After the short summary a full description should follow if neccessary.
    - Where required the arguments that the function should be listed as a bullet list
    - The description must clearly describe the return value that the function should produce, providing simple examples as neccessary to aid the description.
    - The description must list any exceptions that the function shall raise and under what conditions.

 An example in rST format ::

    ==========================================
    Quora Python Beginners - Example Challenge
    ==========================================

    A function that takes two numbers as postional arguments and adds them together, returning the result.

    The function will take two numbers (integers or floats), and return the two numbers added together, with the
    following reservations :

     - If either value is zero the result returned should be zero
     - If either value is negative the result should be zero

    There is no requirement for the function to test the type of either argument.

    Exceptions
    ----------

    The Function is not required to raise any exceptions.

This example is also available as the description of the `example_challenge <QuoraChallengesTestData>`_ from the
QuoraChallengesTestData repository.

The description must be provided within the challenge folder in a file named as 'description.rst'.

In order to test that the description is formatted correctly, use the :ref:`describe function <function_describe>` from the framework.

.. _rST : http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
.. _QuoraChallengesTestData : https://github.com/TonyFlury/QuoraChallengesTestData/example_challenge

.. rubric:: Footnotes
.. [#docstringFormat] https://www.python.org/dev/peps/pep-0257/
