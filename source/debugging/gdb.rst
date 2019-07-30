Debugging with GDB
==================

Renode allows you to debug applications running on emulated machines using `GDB <https://www.gnu.org/software/gdb/>`_.

It uses the GDB remote protocol and allows using the most common GDB functions, like breakpoints, watchpoints, stepping, memory access etc.

The most important difference to debugging on the real hardware, is that the virtual time does not progress when the emulated CPU is halted.
This makes the debugging process transparent for the emulated machines.

Connecting to  GDB
------------------

To start a GDB server on port 3333, run::

    (machine-0) machine StartGdbServer 3333

This allows you to start GDB from an appropriate toolchain and connect to a remote target::

    $ arm-none-eabi-gdb /path/to/application.elf
    (gdb) target remote :3333

Starting emulation
------------------

After GDB connects to Renode, the emulation needs to be started.
Simply telling GDB to continue is not enough to start the time flow, as it would disrupt more complicated multinode scenarios.

There are three ways to start the whole setup.

You can start the emulation manually from Renode's Monitor, typing the usual::

    (machine-0) start

Then, in GDB, run::

    (gdb) continue

Alternatively, GDB's ``monitor`` command may be used to pass the commands to Renode's Monitor::

    (gdb) monitor start
    (gdb) continue

The third option, suited for the simplest scenarios, makes Renode start the whole emulation as soon as GDB connects.
It requires an additional parameter for ``StartGdbServer``, named ``autostartEmulation``::

    (machine-0) machine StartGdbServer 3333 true

Complex scenarios
-----------------

By default, the command ``StartGdbServer`` adds all CPUs of a machine to the newly created server.

It can be also used to add a specific CPU to an existing server, or create a new server with that CPU.
This allows you to create more complex setups, with multiple GDB instances running debug sessions with different CPUs.

To start a GDB server on port 3333 with one CPU, two more paramaters are required - previously mentioned ``autostartEmulation``, and ``cpu``::

    (machine-0) machine StartGdbServer 3333 true sysbus.cpu1

To add a second CPU to that server, run::

    (machine-0) machine StartGdbServer 3333 true sysbus.cpu2

To start a new GDB server on port 3334 with another CPU, run::

    (machine-0) machine StartGdbServer 3334 true sysbus.cpu3

These commands will give you a setup consisting of two GDB servers - on port 3333 with two CPUs, and on port 3334 with one CPU.

Furthermore, the ``StartGdbServer`` command will prohibit you from adding one CPU to more than one GDB server.

If a CPU was added to a GDB server by providing the ``autostartEmulation`` and ``cpu`` parameters, it will be impossible to run the general version of the command on that machine.
