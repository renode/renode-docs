.. _zephyr-ptp-testing:

Testing Zephyr PTP support
==========================

This tutorial will guide you on how to use Renode to run a set of tests verifying Zephyr's `TSN/PTP support <https://en.wikipedia.org/wiki/Precision_Time_Protocol>`_.

Prerequisites
-------------

To start the test you need to download and build Renode according to the :ref:`building instructions <building-from-source>`.

The test suite is using `Robot Framework <https://robotframework.org/>`_ and can be run with a single script.

To create your own Zephyr binaries to be tested, you need to follow `Zephyr's Getting Started Guide <https://docs.zephyrproject.org/latest/getting_started/index.html>`_.

The tests require two Zephyr ELF files built from the ``zephyr/samples/net/gptp`` sample, targeting the ``sam_e70_xplained`` board.

To build them, create two overlay files, one for the Grand Master node, one for the slave.

Config for the Grand Master (gm.conf)::

  CONFIG_NET_GPTP_GM_CAPABLE=y
  CONFIG_ETH_SAM_GMAC_RANDOM_MAC=y

  CONFIG_NET_CONFIG_MY_IPV4_ADDR="192.0.2.1"
  CONFIG_NET_CONFIG_MY_IPV6_ADDR="2001:db8::1"
  CONFIG_NET_GPTP_NEIGHBOR_PROP_DELAY_THR=200000

Config for the slave node (slave.conf)::

  CONFIG_NET_GPTP_GM_CAPABLE=n
  CONFIG_ETH_SAM_GMAC_RANDOM_MAC=y

  CONFIG_NET_CONFIG_MY_IPV4_ADDR="192.0.2.2"
  CONFIG_NET_CONFIG_MY_IPV6_ADDR="2001:db8::2"
  CONFIG_NET_GPTP_NEIGHBOR_PROP_DELAY_THR=200000

Follow the Zephyr documentation to build these samples.
For example, to build the Grand Master application, run::

  west build --board sam_e70_xplained -- -DOVERLAY_CONFIG=gm.conf

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

    ./test.sh --variable ZEPHYR_MASTER_ELF:path/to/zephyr.elf --variable ZEPHYR_SLAVE_ELF:path/to/another/zephyr.elf tests/platforms/SAME70.robot
