.. _zephyr-ptp-testing:

Testing Zephyr PTP support
==========================

This tutorial will guide you on how to use Renode to run a set of tests verifying Zephyr's `TSN/PTP support <https://en.wikipedia.org/wiki/Precision_Time_Protocol>`_.

Prerequisites
-------------

To start the test you need to download and build Renode according to the :ref:`building instructions <building-from-source>`.

The test suite is using `Robot Framework <https://robotframework.org/>`_ and can be run with a single script.

To create your own Zephyr binaries to be tested, you need to follow `Zephyr's Getting Started Guide <https://docs.zephyrproject.org/latest/getting_started/getting_started.html>`_.

The tests require two Zephyr ELF files built from the ``zephyr/samples/net/gptp`` sample, targeting the ``sam_e70_xplained`` board.
One of the binaries, acting as a Grand Master node, must be built with ``CONFIG_NET_GPTP_GM_CAPABLE=y``.
Both binaries must have the ``CONFIG_ETH_SAM_GMAC_RANDOM_MAC=y`` setting.


The test suite
--------------

The suite executes a set of tests running on two SAM E70 nodes, connected via ethernet. The following tests are implemented:

#. node should send a PDelay request packet
#. slave node should accept a Grand Master node by calling a specific Zephyr callback
#. master node should send Announce packets with expected parameters
#. master node should send properly formed Sync and Sync Follow Up packets
#. master node should send Sync packets in valid intervals
#. slave node should sync its clock to master

Running the test
----------------

To start the test, simply run the following command from the Renode root directory::

    ./test.sh tests/platforms/SAME70.robot

This will run the whole suite of tests.
After the test is finished, the result will be stored in ``output/tests/report.html``.

To switch the binaries used in these tests, edit the provided ``.robot`` file.
Alternatively, if you don't want to make any changes, you can use the ``--variable`` switch to specify the files you want to use::

    ./test.sh --variable ZEPHYR_MASTER_FILE:path/to/zephyr.elf --variable ZEPHYR_SLAVE_ELF:path/to/another/zephyr.elf tests/platforms/SAME70.robot
