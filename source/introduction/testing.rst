Testing with Renode
===================

Renode's testing capabilities
---------------------------------

Renode is very well suited to be a part of an automated tests scenario, e.g. run in the background on a CI server.

Renode is integrated with the `Robot Framework <https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#introduction>`_ testing suite and provides user-friendly scripts for running tests.

It comes with a variety of prepared test scripts, but it also allows you to extend them or add new ones.

Running the robot test script
-----------------------------

Running a robot test script in Renode is as simple as executing a single command::

    $ renode-test my_test.robot

The above command will:

* start a Renode instance in the background,
* enable Renode's built-in Robot Framework server (providing an interface between Robot Framework and Renode) on port 9999 (the port number can be changed by the user),
* start the Robot Framework test engine and connect to Renode,
* run the provided ``my_test.robot`` test case,
* print the progress status on the console,
* generate the log and the summary after finishing the test.

Below, you can see an example output::

    Preparing suites
    Started Renode instance on port 9999; pid 2293056
    Starting suites
    Running tests/platforms/LiteX-VexRiscv.robot
    +++++ Starting test 'LiteX-VexRiscv.Timer Test'
    +++++ Finished test 'LiteX-VexRiscv.Timer Test' in 46.79 seconds with status OK
    +++++ Starting test 'LiteX-VexRiscv.I2C Test'
    +++++ Finished test 'LiteX-VexRiscv.I2C Test' in 8.10 seconds with status OK
    Cleaning up suites
    Closing Renode pid 2293056
    Aggregating all robot results
    Output:  /home/antmicro/renode/output/tests/robot_output.xml
    Log:     /home/antmicro/renode/output/tests/log.html
    Report:  /home/antmicro/renode/output/tests/report.html
    Tests finished successfully :)

Note that two entries in the output associated with a single test case appear
- one when the test starts and another when it finishes (useful when running tests in parallel).
The second message contains information about the test's duration and status.

The details of the run can be found in:

* the ``robot_output.xml`` report (suitable for automatic parsing),
* the ``log.html`` and ``report.html`` documents (suitable for an interactive inspection).

Creating the test file
----------------------

Robot Framework uses text files based on a custom syntax to express the test cases.
The details of the grammar can be found in `the official documentation <http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html>`_.
In order for the robot files to work with Renode, proper configuration (explained below) is needed.

Here is an example of a simple robot test file that works with Renode::

    *** Settings *** 
    Suite Setup     Setup 
    Suite Teardown  Teardown 
    Test Teardown   Test Teardown 
    Resource        ${RENODEKEYWORDS} 
     
    *** Test Cases *** 
    Should Print Help 
        ${x}=  Execute Command     help 
               Should Contain      ${x}    Available commands: 

The ``Should Print Help`` test case executes the ``help`` command in Renode's monitor and verifies the result.

Integration with Renode is achieved by adding entries to the settings section.
The ``RENODEKEYWORDS`` variable (initialized by the ``renode-test`` script) contains the path to the `renode-keywords.robot <https://github.com/renode/renode/blob/master/src/Renode/RobotFrameworkEngine/renode-keywords.robot>`_ script responsible for setting up the connection with Renode.
Other settings configure the suite/test setup and teardowns.

It is recommended to copy the above ``Settings`` section to each new robot test file.

Adding new test cases
+++++++++++++++++++++

Each robot test file might contain many test cases.
For general instructions on how to define tests cases, please refer to `the Robot Framework documentation <http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html>`_.
In this section, we will focus on using the Robot Framework-Renode integration.

The Robot Framework-Renode integration layer provides keywords allowing the user to control and inspect the state of the simulation directly from the Robot Framework test file in a similar manner to the built-in keywords.
The `basic keywords <https://github.com/renode/renode/blob/master/src/Renode/RobotFrameworkEngine/RenodeKeywords.cs>`_ allow the user to:

* start the emulation (``Start Emulation``),
* clear the emulation (``Reset Emulation``),
* execute a command in the Monitor (``Execute Command``),
* allocate a file in the Renode temporary folder (``Allocate Temporary File``),
* download a file to the Renode temporary folder (``Download File``),

and more (see the source code for details).

Additionally, Renode provides `a set of keywords for interacting with UART devices <https://github.com/renode/renode/blob/master/src/Renode/RobotFrameworkEngine/UartKeywords.cs>`_.
They allow:

* writing a text to UART (``Send Key To Uart``, ``Write Char On Uart``, ``Write Line To Uart``),
* waiting for a specific line to appear on UART (``Wait For Line On Uart``, ``Wait For Prompt On Uart``),
* waiting for any output on UART (``Wait For Next Line On Uart``),
* waiting for the lack of output on UART (``Test If Uart Is Idle``).

There is also `a set of keywords for interacting with network devices <https://github.com/renode/renode/blob/master/src/Renode/RobotFrameworkEngine/NetworkInterfaceKeywords.cs>`_ that allow:

* waiting for the next outgoing network packet (``Wait For Outgoing Packet``),
* waiting for a specific outgoing network packet (``Wait For Outgoing Packet With Bytes At Index``).

It is possible to extend the Renode-Robot Framework interface by implementing more keywords in C# if necessary.

For reference on how to use the keywords mentioned in this section, see the robot test files that Renode comes with.
 
Advanced usage
--------------

Running many test files with a single command
+++++++++++++++++++++++++++++++++++++++++++++

The example in the previous section presented how to run a single test file (which might still contain many test cases).
It is possible to run many test files and aggregate the results into a single report.
In order to do that, you need to pass many test files as an argument to ``renode-test`` command::

    $ renode-test my_tests.robot additional_tests.robot extra_tests.robot

The tests will be executed in the order the arguments were provided in.

An alternative way is to prepare a ``yaml`` file with the list of tests to execute, e.g.::

    - my_tests.robot
    - additional_tests.robot
    - extra_tests.robot

and to call ``renode-test`` with a special switch::

    $ renode-test -t my_tests.yaml

.. note::

    The yaml notation allows the user to include other yaml files and to group entries that should not be executed in parallel (see the next section).


Running tests in parallel
+++++++++++++++++++++++++

Test cases from a single file will always be executed in serial (in the order they are defined in the file), but it's possible to run tests from different files in parallel.
In order to do that, execute the ``renode-test`` command with a special switch::

    $ renode-test -j12 my_tests.yaml

This will allow you to run up to 12 Renode instances, each one running test cases from a different file.
Using the ``yaml`` file allows grouping entries that should not be executed in parallel (because, e.g., they use a shared resource like a port number)::

    - my_tests.robot
    - my_group:
        - my_test2.robot
        - my_test3.robot

In the example above, ``my_test2.robot`` will be executed before ``my_test3.robot`` but in parallel with ``my_tests.robot``.

You can also pass many test files as arguments (i.e., without the ``yaml`` file), but this won't allow you to do the grouping::

    $ renode-test -j3 my_tests.robot my_tests2.robot my_tests3.robot


Stopping on error
+++++++++++++++++

By default, ``renode-test`` will run all the provided test cases.
It is possible, however, to stop the execution on the first encountered error.
In order to do that, run the ``renode-test`` script with::

    $ renode-test --stop-on-error my_tests.robot


Running multiple instances of renode-test at the same time
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Renode communicates with the Robot Framework executor over a network socket.
This means that running two ``test-renode`` instances at the same time will result in a network port conflict.

In order to avoid that, you can explicitly specify the port number to be used for the communication between the Robot Framework and Renode::

    $ renode-test -P 9997 my_test.robot &
    $ renode-test -P 9998 my_test2.robot &


Repeating tests
+++++++++++++++

It is possible to run the specified tests multiple times using::

    $ renode-test -n 10 my_test.robot

This will repeat all the test cases from ``my_tests.robot`` 10 times.

Running selected fixtures
+++++++++++++++++++++++++

It is possible to run only selected test cases from the file using::

    $ renode-test -f "*GDB*" my_tests.robot

In the example above only test cases with ``GDB`` in their name will be run.

Running tests interactively
+++++++++++++++++++++++++++

By default, ``renode-test`` command will run tests in the background and just report results on the console.
It is possible, however, to enable printing log messages to the console in the same way as when running the ``renode`` command::

    $ renode-test --show-log my_tests.robot

.. note::

    This will cause the test progress report messages to be mixed with the log messages.

What's more, it is also possible to show the Monitor and analyzers windows and interact with them::

    $ renode-test --enable-xwt my_tests.robot

.. note::

    Interacting with the running test may influence the results.

Saving state of failed tests
++++++++++++++++++++++++++++

Renode's testing framework allows the automatic creation of snapshots of failed tests in order to load them later to inspect the state of the simulation and/or run them further.
This feature is especially helpful in non-interactive CI environments.

To enable automatic creation of snapshots for failed tests, set the ``RENODE_CI_MODE`` environment variable before running the ``renode-test`` command::

    $ RENODE_CI_MODE=YES renode-test my_test.robot

Each time the snapshot is created, it will be given a name corresponding to the failed test and you will see the message in the console informing you about the path to it.
All snapshots will be saved in the ``output/tests/snapshots`` directory.

.. note::

    Enabling the CI mode will also influence the way external resources are handled - the binaries cache will be disabled, so each external file will be downloaded every time it's referenced.

Inspecting failed tests interactively
+++++++++++++++++++++++++++++++++++++

With Renode, it is possible to stop the execution of the test suite in order to interactively debug a failed test case using the standard Renode interface (monitor, UART analyzers, etc).

To enable this feature, run the ``renode-test`` command with the following switch::

    $ renode-test --debug-on-error my_test.robot

This will result in pausing the execution of the test suite on error, displaying the Renode Monitor and peripheral analyzers and allowing the user to inspect the state of the simulation.
Once the interactive session is done, it's possible to resume the execution of tests by pressing a button in a prompt window.


.. note::

    This feature is currently not available in headless environments.
