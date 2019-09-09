==========================
Developer Guide - Overview
==========================

This section documents how experienced developers can implement their own challenges for either `Python Beginners`_ or `Python Programmers`_.

Pre requisites
--------------
    - You are a known contributor to either `Python Beginners`_ or `Python Programmers`_ spaces on `Quora`_
    - You have git on your developement machine
    - you have an account on Git Hub.

Process Overview
----------------
There is a simple 8 step process to provide your own challenges :

1. Create a GIT fork of `QuoraChallenges_GitHub`_ and clone that fork to your local computer.
2. Create a new developement branch in your local copy.
3. Create a new folder at the top level of the repository - the name of folder is the chosen name for the challenge.
4. Within the new folder create the following files :doc:`description.rst<description>`, :doc:`testdata.json<testdata>`, and optionally a :doc:`compare.py<compare>`
5. Edit the Readme.rst to add your challenge.
6. Once the challenge content is complete - commit and push the changes to your git hub fork.
7. Request a pull request to merge your branch into the main repository.
8. Once the merge has been completed - publicise your challenge in the appropriate space.

When compiling your challenge, please keep in mind at all times the target audience. The `Python Beginnners` space is
intended for those developers who are just starting out with Python and likely just starting out with development. It is
likely that they wont be up to speed with most data structure and algorithms. Challenges aimed at the developers in
`Python Programmers`_ (who generally have skill level intermediate and beyond) will be much less common and should be
more likely to admit more than one style of solution.

.. toctree::
    description
    testdata
    compare

.. _Python Beginners : https://www.quora.com/q/python-beginners
.. _Python Programmers : https://www.quora.com/q/python-programmers
.. _QuoraChalennges_GitHub : https://github.com/TonyFlury/QuoraChallengesTestData