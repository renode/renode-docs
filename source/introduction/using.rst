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

The ``help`` command provides a list of available commands with a short description.
It provides detailed information when used with another built-in command as an argument, e.g., ``help logLevel``.

Typing any command with wrong or incomplete arguments will also print a help string.

For ease of use, a partial autocompletion feature is available.
Just press :kbd:`Tab` once to complete the current command or twice to see all available suggestions.

For commands with file arguments, the ``@`` sign represents a path to a file - for convenience, Renode provides autocompletion also for filenames.

.. note::

   After a ``@`` sign, the Monitor will suggest files both in the current working directory from which Renode was run and the Renode installation directory as fallback - the former take precedence in case of ambiguity.

The most common commands (e.g., ``start`` or ``quit``) provide short, usually single-letter, aliases (so ``s`` and ``q``, respectively).

The CLI provides a command history (arrows :kbd:`up`/:kbd:`down`) with interactive search (:kbd:`Control-r`) to easily re-execute previous commands.

Pasting with :kbd:`Control-Shift-v`, as well as via the context menu on right click, is also available.
To erase the current command and return to a clean prompt, use :kbd:`Control-c`.

Basic interactive workflow
--------------------------

When running Renode interactively, the user would normally start with creating the emulation through a sequence of commands building up, configuring and connecting the relevant emulated (guest) platform or platforms (called "machines").

This is normally done using nested :ref:`scripts` which help encapsulate some of the repeatable elements in this activity (normally, the user will want to create the same platform over and over again in between runs, or even script the execution entirely).

When the emulation is created and all the necessary elements (including e.g. binaries to be executed) loaded, the emulation itself can be started - to do this, use the ``start`` command in the Monitor.

At this point, you will be able to see lots of information about the operation of the emulated environment in the log window, extract additional information and manipulate the running emulation using the Monitor (or plugins such as :doc:`Wireshark <../networking/wireshark>`) - as well as interact with the external interfaces of the emulated machines like UARTs or Ethernet controllers.

For some typical commands useful in creating and manipulating machines from the Monitor, you can refer to the :ref:`working-with-machines` section.

Some more commands and info on interacting with the emulation can be found in the :ref:`basic-control` section.

.. _scripts:

.resc scripts
-------------

To load a script (which in Renode will typically use the ``.resc`` extension), use::

    include @/path/to/script.resc

If in the above command you use ``start`` (or just ``s``) instead of ``include``, the emulation will start immediately after loading the script.

.. note::

   Remember about path autocompletion using the :kbd:`Tab` key after ``@``, as described in the :ref:`previous section <monitor>`.

Scripts can ``include`` further scripts which is useful e.g. to create complex multinode setups.

Renode ships with a number of demo scripts which are a great entry point - to run your first demo, proceed to the :doc:`demo` chapter.

Configuring the user interface
------------------------------

The appearance of the user interface can be customized via the user
configuration file ``config``. It is located in directory ``~/.config/renode``
on Unix-like systems and in ``AppData\Roaming\renode`` on Windows.

In the section ``[termsharp]`` the following settings are available:

append-CR-to-LF
    this setting controls if a carriage return is appended to each line feed.
    Allowable values are ``true`` and ``false``. The default value is ``true``.

font-face
    name of the TrueType font used in the log and monitor windows. The default
    value is ``Roboto Mono``.

font-size
    font size in points. The default value is 12 on Windows and 10 on Linux.

window-width
    initial width (in pixels) of the log and monitor windows

window-height
    initial height (in pixels) of the log and the monitor windows
