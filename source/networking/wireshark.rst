Inspecting the traffic with Wireshark
=====================================

`Wireshark <https://www.wireshark.org>`_ is an open source network packet analyzer.
It can be used to sniff the network traffic between emulated nodes and/or the host network interface.

Renode uses the libpcap format to provide data to Wireshark.

Logging the whole traffic
-------------------------

To log the network traffic to Wireshark, you must decide if you want to focus on the wireless or ethernet network.

This limitation is inherent to the libpcap format, but in reality it is rarely a concern.

To log all traffic transferred over the wired network, run::

    (monitor) emulation LogEthernetTraffic

This creates a new object available in the emulation: ``host.wireshark-allEthernetTraffic``.

The Wireshark window will open automatically when the first ``Switch`` object becomes available.

You can start it manually (e.g. after you close the Wireshark window) with::

    (monitor) host.wireshark-allEthernetTraffic Run

Similarly, to log the traffic of a wireless network, run::

    (monitor) emulation LogWirelessTraffic

This command creates a new ``host.wireshark-allWirelessTraffic`` object.

Observing a specific interface
------------------------------

Renode allows you to inspect the traffic of a specific switch or wireless medium.
You can also limit the observation to a specific interface connected to that switch or medium.

To enable logging on a ``switch`` object, run::

    (monitor) emulation LogToWireshark switch

To observe only the ``sysbus.ethernet`` interface connected to ``switch``, run::

    (machine-0) emulation LogToWireshark switch sysbus.ethernet

The names of Wireshark objects created depend on the machine name, the switch name and the interface name.
In the above case Renode creates an object named ``host.wireshark-switch-machine-0-sysbus-ethernet``.
