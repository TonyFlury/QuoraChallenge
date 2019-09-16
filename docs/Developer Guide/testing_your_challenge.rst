============================================
Testing Your challenge Solution and TestData
============================================

By default the framework will download the description and data from the `QuoraChallengesTestData`_ repository,
looking for the relevant folder in that repository. Clearly this only works when challenge information has been published
which means that the pull request has been merged into the master branch.

Ideally you need to test your description formats correctly, and that the test data is both formatted correctly and will
correctly prove that the Entrants function meets the requirements before attempting the pull request. You can accomplish
this by using the ``_directory`` argument on the :ref:`function_describe`, :ref:`function_autotest` and :ref:`function_testdata`.

The ``_directory`` argument allows the developer to specify the top-level directory of their challenges under development
 - i.e. the parent of the challenge directory that contains the description.rst and testdata.json files.

For example if the directory structure looks like this :

.. image:: ../images/FileDirectory.png

then to test your description :

.. code-block:: pycon

    >>> import quorachallenge as qc
    >>> qc.describe('my_challenge', _directory='~/Development/QuoraChallengesTestData')

Similarly, to test your function (called examplar) :

.. code-block:: python

    import quorachallenge as qc
    qc.AutoTest('my_challenge', _directory='~/Development/QuoraChallengesTestData')(examplar)

And to display your test data :

.. code-block:: python

    import quorachallenge as qc
    qc.testdata('my_challenge', _directory='~/Development/QuoraChallengesTestData')

.. _QuoraChallengesTestData : https://github.com/TonyFlury/QuoraChallengesTestData
