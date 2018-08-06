Running your first demo
=======================

Your Renode installation contains a number of example scripts, located in the `scripts/ directory <https://github.com/renode/renode/tree/master/scripts>`_  (for example, if you installed from Linux packages, this will be in ``/opt/renode/scripts`` on your PC).

You can run any of those demos using the ``include`` or ``start`` command (``i`` and ``s`` for short) with the script's path (by default relative to the Renode installation directory and your current working directory) as a parameter.
For example, run a single node STM32F4 Discovery demo as follows::

   s @scripts/single-node/stm32f4_discovery.resc

Remember about :kbd:`Tab` autocompletion, which will hint you what demos are available.

The binaries for the demos are hosted on our servers, and can be replaced with your own by setting the ``$bin`` variable before loading the script (or changing its value inside the script).

You are free to copy any of the provided demo scripts to your preferred directory and modify them as necessary to match your needs, they should work even from within a different path as they typically only use paths relative to the Renode installation directory.

You can also run a script by passing its path to the ``renode`` command, this will be interpreted as running Renode and using ``include @/path/to/script.resc`` (note that you will have to start the emulation manually).
