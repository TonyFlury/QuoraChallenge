=======================================================
Quora Challenge: Quora Challenge Framework
=======================================================

Welcome to the User and contributor documentation for the Quora Python Challenge Framework.

This framework supports the programming challenges as published from time to time in either `Python Beginners`_ or `Python Programming`_ spaces on `Quora`_.

It is entirely possible to complete the challenges without using this framework, though the framework does provide a few useful features:

 - A function :ref:`describe(challenge_name,..) <function_describe>` which provides easy to access description of the challenge, without needing to access the original post on Quora.
 - A decorator :ref:`Autotest(challenge_name,..) <function_AutoTest>` which will automatically test the function being decorated and report both test failures and any execptions raised by the function.

For a short tutorial of how to use the framework see :doc:`Gettng Started <GettingStarted>`

.. note::
    The Quora Challenge Framework is only supported on Python 3.6 onwards. Versions for Python 3.5 and earlier, and Python 2 do not exist and are highly unlikely to be produced.

Suggested reading order
-----------------------

For someone undertaking the challenges :

.. toctree::
    :maxdepth: 2

    Installation
    GettingStarted
    QuoraChallengeFramework

This documentation set also describes how experienced developers can submit new challenges :

.. toctree::
    :maxdepth: 2

    Developer Guide/overview

.. note::
  Every care is taken to try to ensure that this code comes to you bug free.
  If you do find an error - please report the problem on :

    - `GitHub Issues`_
    - By email to : `Tony Flury`_


.. _Github Issues: http://github.com/TonyFlury/quorachallenge/issues/new
.. _Tony Flury : mailto:anthony.flury@btinternet.com?Subject=quorachallenge%20Error
.. _Python Beginners : https://www.quora.com/q/python-beginners
.. _Python Programming : https://www.quora.com/q/python-programming
.. _Quora : https://www.quora.com/