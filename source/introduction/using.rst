Using Renode
============

Running and quitting Renode
---------------------------

To start Renode, use the ``renode`` command in your operating system's terminal.

The current terminal will now contain the Renode log window, and a new window will pop up for "the Monitor" - the CLI for Renode.

To quit Renode gracefully and close all the associated windows, use the ``quit`` command in the Monitor at any time.

.. _monitor:

Monitor (Renode CLI)
--------------------

The Monitor is used to interact with Renode and control the emulation.
It exposes a set of basic commands and allows the user to access emulation objects.
Using the Monitor, the user can execute actions provided by those objects as well as examine and modify their state.

The Monitor comes with several built-in features to make the user experience similar to a regular terminal application.

Using built-in commands
+++++++++++++++++++++++

The ``help`` command provides a list of available commands with a short description::

	(monitor) help
	Available commands:
	Name              | Description
	================================================================================
	alias             : sets an alias.
	allowPrivates     : allow private fields and properties manipulation.
	analyzers         : shows available analyzers for peripheral.
	commandFromHistory: executes command from history.
	createPlatform    : creates a platform.
	currentTime       : prints out and logs the current emulation virtual and real time
	...

You can get more detailed information about a selected command by using the ``help`` command with another built-in command as an argument::

	(monitor) help analyzers
	Usage:
	------
	analyzers [peripheral]
	lists ids of available analyzer for [peripheral]
	analyzers default [peripheral]
 	writes id of default analyzer for [peripheral]

Typing any command with wrong or incomplete arguments will also print a help string.

For ease of use, a partial autocompletion feature is available.
Just press :kbd:`Tab` once to complete the current command or twice to see all available suggestions.

For commands with file arguments, the ``@`` sign represents a path to a file; for convenience, Renode also provides autocompletion for filenames.

.. note::

   After a ``@`` sign, the Monitor will suggest files both in the current working directory from which Renode was run and in the Renode installation directory as a fallback - the former taking precedence in case of ambiguity.

The most common commands (e.g., ``start`` or ``quit``) provide short, usually single-letter, aliases (so ``s`` and ``q``, respectively).

The CLI provides a command history (arrows :kbd:`up`/:kbd:`down`) with interactive search (:kbd:`Control-r`) to easily re-execute previous commands.

Pasting with :kbd:`Control-Shift-v`, as well as via the context menu on right click, is also available.
To erase the current command and return to a clean prompt, use: :kbd:`Control-c`.

Basic interactive workflow
--------------------------

When running Renode interactively, the user would normally start by :ref:`creating the emulation <working-with-machines>` through a sequence of commands building up, configuring, and connecting the relevant emulated (guest) platform or platforms (called "machines").

This is normally done using nested :ref:`scripts` which help encapsulate some of the repeatable elements in this activity (normally, the user will want to create the same platform over and over again in between runs, or even script the execution entirely).

When the emulation is created and all the necessary elements (including e.g. binaries to be executed) are loaded, the emulation itself can be started - to do this, use the ``start`` command in the Monitor.

At this point, you will be able to see lots of information about the operation of the emulated environment in the :ref:`logger <using-logger>` window, extract additional information and manipulate the running emulation using the Monitor (or plugins such as :doc:`Wireshark <../networking/wireshark>`) - as well as interact with the external interfaces of the emulated machines like `UARTs <https://renode.readthedocs.io/en/latest/networking/uart-hub.html>`_ or :ref:`Ethernet controllers <wired-network>`.

For some typical commands useful in creating and manipulating machines from the Monitor, you can refer to the :ref:`working-with-machines` section.

Some more commands and info on interacting with the emulation can be found in the :ref:`basic-control` section.

.. _scripts:

.resc scripts
-------------

Renode scripts (.resc) enable you to encapsulate repeatable elements of your project (like creating a machine and loading a binary) to conveniently execute them multiple times.
The syntax used in the ``.resc`` files is the same as that of the Monitor.

Renode has many built-in ``.resc`` files, like this `Intel Quark C1000 script <https://github.com/renode/renode/blob/master/scripts/single-node/quark_c1000.resc>`_.

To load a script (which in Renode will typically use the ``.resc`` extension), use::

    include @/path/to/script.resc

If in the above command you use ``start`` (or just ``s``) instead of ``include``, the emulation will start immediately after loading the script.

.. note::

   Remember about path autocompletion using the :kbd:`Tab` key after ``@``, as described in the :ref:`previous section <monitor>`.

Scripts can ``include`` further scripts, which is useful e.g. to create complex multinode setups like `nRF52840 BLE <https://github.com/renode/renode/blob/master/scripts/multi-node/nrf52840-ble-zephyr.resc>`_.

`Built-in Renode demo scripts <https://github.com/renode/renode/tree/master/scripts>`_ are a great entry point - to run your first demo, proceed to the :doc:`demo` chapter.
