Introduction
------------

Installing Renode
.................

The installation process of the Renode framework depends on the operating system.
Please use the packages available on `Renode's Github <https://github.com/renode/renode/releases/latest>`_.

The system requirements are described in the `Renode project README <https://github.com/renodeio/renode/blob/master/README.rst#installation>`_.

For instructions how to install Renode from sources (advanced users) see :ref:`this document <building-from-source>`.

Using Renode
............

To start Renode, use the ``renode`` command.

You will see "the Monitor" - the CLI for Renode.

The Monitor is used to interact with Renode and control the emulation.
It exposes a set of basic commands and allows the user to access emulation objects.
Using the Monitor, the user can execute actions provided by those objects as well as examine and modify their state at any instant.

The Monitor comes with several built-in features to make using it similar to the way you'd use a terminal application.

The ``help`` command provides a list of available commands with a short description.
It provides detailed information when used with another built-in command as an argument, e.g., ``help logLevel``.

Typing any command with wrong or incomplete arguments will also print a help string.

For ease of use, a partial auto-completion feature is available.
Just press ``<tab>`` once to complete the current command or twice to see all available suggestions.

The most common commands (e.g., ``start`` or ``quit``) provide short, usually single-letter, aliases.

The CLI provides commands history (arrows :kbd:`up`/:kbd:`down`) with interactive search (:kbd:`Control-r`) to easily re-execute previous commands.

Pasting with :kbd:`Control-Shift-v`, as well as via the context menu upon right click, is also available.
To cancel entering of the current command and return to a clean prompt, use :kbd:`Control-c`.

You can type the commands interactively or load a script using::

    include @/path/to/script

In Renode, the "@" sign represents a path to a file.

To start the loaded emulation, run ``start``; to quit Renode type ``quit``.
More on interacting with the emulation can be found in the :ref:`basic-control` section.

Renode supports emulation of multiple nodes - for details see the :ref:`working-with-machines` section.

There is also a :ref:`tutorial <miv-tutorial>` that wraps all the information in a real-world usage scenario.
