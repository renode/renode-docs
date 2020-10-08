UART-based connections
======================

Renode allows connecting boards into a network using UART devices that exchange data.

Creating a hub
--------------

UART devices can be connected together using UART hubs.

To create a hub named ``uartHub``, execute::

    (monitor) emulation CreateUARTHub "uartHub"

Connecting UART devices
-----------------------

In order for UART devices to be able to communicate, they must be connected to a common UART hub.

Exactly as in the case of :ref:`the wired network <wired-network>`, use ``connector`` to connect them together::

    (monitor) mach set 0
    (machine-0) connector Connect sysbus.uart uartHub
    (machine-1) mach set 1
    (machine-1) connector Connect sysbus.uart uartHub

Disconnecting UART devices
--------------------------

You can also disonnect a device from a hub with::

    (machine-1) connector Disconnect sysbus.uart uartHub

Running the simulation
----------------------

The UART hub is created in a paused state, which means it won't transfer any data between devices.
To enable the communication it must be started first.
It happens automatically when starting the whole simulation, with::

    (monitor) start

or can be triggered manually, with::

    (monitor) uartHub Start

From this moment on data sent to ``sysbus.uart`` on ``machine-0`` will be received by ``sysbus.uart`` on ``machine-1`` and vice versa.

.. note::

    You can also stop a hub at any moment, with::

        (monitor) uartHub Pause

In order to ensure the determinism of the simulation, bytes sent over an uartHub are buffered and delivered to the receiver at predefined times.
Please, note that this might lead to slight delays in the communication.
The maximum delay is controllable by the ``quantum`` parameter.
For details on how the synchronization works and how to configure it, refer to :ref:`the synchronization section <time-framework_synchronization>` of the documentation.
