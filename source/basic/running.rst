Running Renode in different modes
=================================

By default Renode runs in GUI mode.
When started, it opens a new window for :ref:`the Monitor <monitor>` and additional windows for different analyzers (e.g., UART).

It is, however, possible to start Renode in other modes too. 
Below we present alternative ways of running and interacting with Renode.

Telnet mode
-----------

Renode can be started with the Monitor interface available over a network socket instead of a window.
In this mode it will still open other windows locally, but the simulation can be controlled remotely.

To start Renode in telnet mode, run it with the ``-P`` switch::

    $ renode -P 1234
    17:01:20.6362 [INFO] Loaded monitor commands from: /home/antmicro/renode/scripts/monitor.py
    17:01:20.6800 [INFO] Monitor available in telnet mode on port 1234
    17:02:17.2373 [INFO] Script: hello

After that you can connect to it with::
  
   $ telnet 127.0.0.1 1234
   Trying 127.0.0.1...
   Connected to 127.0.0.1.
   Escape character is '^]'.
   Renode, version 1.12.0.33182 (0cd6e174-202108311750)

   (monitor) log "hello"
   (monitor)

You can disconnect from the telnet session and the Renode instance will continue running in the background.

In order to close Renode opened in telnet mode, you have to connect to it and issue the ``quit`` command.

Headless mode
-------------

Renode can be built/run in headless mode that doesn't require any graphical environment (e.g., X11) to be present in the system.
This mode is especially useful when running simulation in a CI environment.

Building for headless use
+++++++++++++++++++++++++

To build Renode in a headless environment use the ``--no-gui`` switch::

    $ ./build.sh --no-gui

Running in a headless environment
+++++++++++++++++++++++++++++++++

Even if you have Renode with a compiled-in GUI support (the default configuration), you can start it in headless mode with::

    $ renode --disable-gui

It is similar to telnet mode as the Monitor will be available on port 1234 by default (the port number can be changed with the ``-P`` switch).
The difference is that in headless mode no graphical windows will be created for analyzers - e.g., UART analyzers will output to log by default.

Console mode
------------

It is possible to start Monitor in the same console window where Renode is started.
In this mode the prompt will be intertwined with log messages::

    $ renode --console
    16:54:37.2215 [INFO] Loaded monitor commands from: /home/antmicro/renode/scripts/monitor.py
    Renode, version 1.12.0.33182 (0cd6e174-202108311750)

    (monitor) log "hello"
    16:54:41.0966 [INFO] Script: hello
    (monitor)

.. note::
    Console mode can be mixed together with headless mode by passing both ``--console`` and ``--disable-gui``.

UART interactions in the Monitor
--------------------------------

With the ``uart_connect`` command it is possible to switch between the Monitor and an interactive UART session::

    [...]
    (machine-0) uart_connect sysbus.uart0
    Redirecting the input to sysbus.uart0, press <ESC> to quit...

    Welcome to buildroot!
    master login: root
    # ls
    # ls /
    bin      etc      lib      media    opt      root     sbin     tmp      var
    dev      home     linuxrc  mnt      proc     run      sys      usr
    # Disconnected from sysbus.uart0
    (machine-0)

In this mode all input from the user is directed to UART and all output from UART is displayed in place of the Monitor prompt.
This works in all Monitor modes (window, telnet, console).

