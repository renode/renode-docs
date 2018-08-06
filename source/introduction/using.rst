Using Renode
============

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

You can type the commands interactively or load a script (which in Renode typically use the ``.resc`` extension) using::

    include @/path/to/script.resc

In Renode, the "@" sign represents a path to a file.
If in the above command you use ``start`` (or just ``s``) instead of ``include``, the emulation will start immediately after loading the script.

To start a previously loaded emulation, use ``start`` without any parameters. To quit Renode type ``quit``.

Some more commands and info on interacting with the emulation can be found in the :ref:`basic-control` section.

Renode supports emulation of multiple nodes - for details see the :ref:`working-with-machines` section.

There is also a :ref:`tutorial <miv-tutorial>` that wraps all the information in a real-world usage scenario.

Running your first demo
-----------------------

Your Renode installation contains a number of example scripts, located in the `scripts/ directory <https://github.com/renode/renode/tree/master/scripts>`_  (if you installed from Linux packages, this will be in ``/opt/renode/scripts`` on your machine).

You can run any of those demos using the ``include`` or ``start`` command with the script's path (by default relative to the Renode root directory - for Linux package installations ``/opt/renode`` and your current working directory)  as a parameter.
For example, run a single node STM32F4 Discovery demo as follows::

   s @scripts/single-node/stm32f4_discovery.resc

Remember about tab auto-completion, which will hint you what demos are available.

The binaries for the demos are hosted on our servers, and can be replaced with your own by setting the ``$bin`` variable before loading the script (or changing its value inside the script).

You are free to copy any of the provided demo scripts to your preferred directory and modify them as necessary to match your needs, they should work even from within a different path as they typically only use paths relative to the Renode installation directory.

You can also run a script by passing its path to the ``renode`` command, this will be interpreted as running Renode and using ``include @/path/to/script.resc`` (note that you will have to start the emulation manually).
