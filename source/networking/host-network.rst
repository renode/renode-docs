Connecting to the host network
==============================

Renode allows you to connect a host network interface to :ref:`an emulated wired network <wired-network>`.

To do that you need to be able to create a ``TAP`` interface.
Renode will try to create one, provided you have sufficient privileges.

.. note::
   Host-guest networking is currently available on Linux and macOS only.

Regarding time flow
-------------------

All devices emulated in Renode operate in :ref:`virtual time <time-framework>`, which is typically slower than the real time flow.
Moreover, network packets are delivered in periodical synchronisation points, delaying the communication even further.

This means that time constraints (e.g. timeouts) placed by applications trying to connect to the emulated network from the host may need to be altered to take these delays into account.

Opening a TAP interface
-----------------------

To create and open a TAP interface, that will be listed on your host system as ``tap0`` and inside Renode as ``host.tap``, run::

    (monitor) emulation CrateTap "tap0" "tap"

If you want the interface to be retained after Renode closes, add a ``true`` parameter::

    (monitor) emulation CrateTap "tap0" "tap" true

Depending on your system configuration, you may be asked for a password to open the interface.

.. note::
   The newly created interface needs to be enabled configured on your host machine.

   By default it has no IP address assigned and is in ``down`` state.

   Please refer to your system documentation for further instructions.

Connecting TAP interface switch
-------------------------------

Assuming you have already :ref:`configured the emulated network <wired-network>`, you can connect a TAP interface to a ``switch`` device by running::

    (monitor) connector Connect host.tap switch

Starting the interface
----------------------

The TAP interface is created as "paused".
To enable communication with the host system you must start it manually, either by running::

    (monitor) start

or, if your emulation is already started, with::

    (monitor) host.tap Start