.. _host-network:

Connecting to the host network
==============================

Renode allows you to connect a host network interface to :ref:`a simulated wired network <wired-network>`.

To do that you need to be able to create a ``TAP`` interface.
Renode will try to create one, provided you have sufficient privileges.

Regarding time flow
-------------------

All devices simulated in Renode operate in :ref:`virtual time <time-framework>`, which is typically slower than the real time flow.
Moreover, network packets are delivered in periodical synchronisation points, delaying the communication even further.

This means that time constraints (e.g. timeouts) placed by applications trying to connect to the simulated network from the host may need to be altered to take these delays into account.

Using TAP interface on Windows
------------------------------

In order to create a TAP device on Windows, a third-party driver, that is a part of `OpenVPN project <https://openvpn.net/community-downloads/>`_, has to be installed.
The feature has been specifically tested with ``OpenVPN 2.5.6``.

Opening a TAP interface
-----------------------

To create and open a TAP interface which will be listed on your host system as ``tap0`` and inside Renode as ``host.tap``, run::

    (monitor) emulation CreateTap "tap0" "tap"

If you want the interface to be retained after Renode closes, add a ``true`` parameter::

    (monitor) emulation CreateTap "tap0" "tap" true

Depending on your system configuration, you may be asked for a password to open the interface.

.. note::
   The newly created interface needs to be enabled and configured on your host machine.

   By default it has no IP address assigned and is in ``down`` state.

   Please refer to your system documentation for further instructions.

Connecting TAP interface switch
-------------------------------

Assuming you have already :ref:`configured the simulated network <wired-network>`, you can connect a TAP interface to a ``switch`` device by running::

    (monitor) connector Connect host.tap switch

Starting the interface
----------------------

The TAP interface is created as "paused".
To enable communication with the host system you must start it manually, either by running::

    (monitor) start

or, if your emulation is already started, with::

    (monitor) host.tap Start

Transferring files from host
----------------------------

If you successfully created a TAP interface, files can be transferred from the host computer to emulation using ``wget``.
To do it you will need to use an IP address associated with the TAP interface on the host machine, for example::

	wget http://192.168.100.1/home/user/file.txt

.. note::

    There are other methods of file transfer: :ref:`built-in TFTP server and Virtio <sharing-files>`.
    Those methods are recommended if you want to avoid the limitations of the host-guest networking via TAP.
