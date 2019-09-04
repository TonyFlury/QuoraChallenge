==========================
Developer Guide - Overview
==========================

This section documents how experienced developers can implement their own challenges for either `Python Beginners`_ or `Python Programmers`_.

Pre requisites
--------------
    The pre-requisites are that you have git and have an account on Git Hub.

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

.. toctree::
    description
    testdata
    compare

.. _Python Beginners : https://www.quora.com/q/python-beginners
.. _Python Programmers : https://www.quora.com/q/python-programmers
.. _QuoraChalennges_GitHub : https://github.com/TonyFlury/QuoraChallengesTestData