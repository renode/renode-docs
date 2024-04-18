.. _wireless-network:

Setting up a wireless network
=============================

Connecting nodes in a wireless network in Renode is as easy as creating :ref:`wired networks <wired-network>`.

Just like with a ``Switch`` object, you can create an abstraction of ``Wireless Medium``, to connect radio interfaces to.

.. _creating-wireless-medium:

Creating a wireless medium
--------------------------

Renode allows you to create multiple virtual wireless media, separated from each other.
The exchanged packets are not transfered between these media, so you can treat this mechanism as means for physical separation which may help you with debugging of your wireless setup.

The network traffic is not affected by the number of nodes connected to one wireless medium.

Renode supports two types of wireless media: ``IEEE802_15_4Medium`` and ``BLEMedium``.
Each one creates an abstration of different type of wireless connection. They're using IEEE802_15_4 standard and Bluetooth Low Energy accordingly.

To create an IEEE802_15_4 medium called ``wireless``, run::

    (monitor) emulation CreateIEEE802_15_4Medium "wireless"

Analogously for a BLE medium::
   
    (monitor) emulation CreateBLEMedium "wireless"

Connecting interfaces
---------------------

To connect an interface to a wireless medium you have to set a proper :ref:`machine context <machine-context>`.

Then, use the ``connector`` mechanism to attach the interface::

    (machine-0) connector Connect sysbus.radio wireless

Although it is not a common setup, each interface can be connected to many media at the same time.

Disconnecting interfaces
------------------------

You can disconnect network interfaces from a wireless medium by running::

    (machine-0) connector Disconnect sysbus.radio wireless

To disconnect from all connected wireless media, use::

    (machine-0) connector DisconnectFromAll sysbus.radio

Positioning the nodes
---------------------

A wireless medium uses 3D coordinates, without any specified unit of distance, to position the connected nodes.

To set a position of a node to coordinates {X = 3, Y = 5, Z = -8.5}, run::

    (machine-0) wireless SetPosition sysbus.radio 3 5 -8.5

Again, the unit of these coordinates is not determined, so it's the user's responsibility of keeping them consistent in the emulation.

Controlling the traffic
-----------------------

By default, the wireless medium delivers all packets to all connected interfaces.
This can be, however, configured, depending on your needs.

Renode exposes an abstraction of ``Medium Functions``.
Each medium function can accept a set of parameters to decide whether a packet exchanged between two nodes (knowing the positions of the sender and the receiver) will be successfuly delivered or not.

Renode provides three medium functions by default:

  * ``SimpleWirelessFunction``

    The default setting, delivering all packets to all connected nodes.

  * ``RangeWirelessFunction``

    This function accepts a parameter indicating the maximal cartesian range between nodes.

    If the nodes are within this range, all packets are delivered successfuly.
    If they are not within range, the communication is not possible.

  * ``RangeLossWirelessFunction``

    This function introduces a probabilistic loss of packets increasing gradually with the distance between nodes.

    Given three parameters, ``lossRange`` (in distance units), ``txRatio`` and ``rxRatio`` (both ranging from 0 to 1.0, inclusively), each packet is subject to two tests.

    The first test determines if the transmission is successful (with probability ``p >> txRatio``).

    The second test takes the distance between the sender and the receiver and calculates the success ratio according the the formula: ``1 - ((distance/lossRange) * (1 - rxRatio))``.

    .. note::
       Keep in mind that even though the ``RangeLossWirelessFunction`` relies on probability, you can still configure the RNG seed with ``emulation SetSeed`` to preserve determinism of execution.
