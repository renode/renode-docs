.. _using-logger:

Using the logger
================

The first window that appears after starting Renode is dedicated to the logger.

There are many logging options you can use to improve your experience with the presented information.

.. _log-level:

Logging level
-------------

There are five available logging levels:

* NOISY (-1),
* DEBUG (0),
* INFO (1),
* WARNING (2),
* ERROR (3).

You can select which messages are logged using the ``logLevel`` command.
Each emulation object can be configured separately.
Also each logger backend (e.g. :ref:`log file <log-file>`) can have its own configuration.

By default, messages from all levels but the NOISY level are logged.

To set the global log level to NOISY, type::

    (machine-0) logLevel -1

To change the log level only for a selected peripheral (in this case - the UART device), type::

    (machine-0) logLevel -1 sysbus.uart

Please be advised that increasing the number of logged messages may affect the performance of the emulation.

The current log level can be verified by running ``logLevel`` without parameters.

This is the output of this command after some configuration::

    (machine-0) logLevel
    Currently set levels:
    Backend           | Emulation element                   | Level
    =================================================================
    console           :                                     : DEBUG
                      : machine-0:sysbus.plic               : ERROR
                      : machine-0:sysbus.uart               : NOISY
    -----------------------------------------------------------------

.. _log-file:

Logging to file
---------------

To analyze the output from a long-running emulation, it is often a good idea to redirect the log to a file.

To achive that, use the ``logFile`` command::

    (machine-0) logFile @some_file_name

This will not disable the console logger, but will add a new sink, to be configured separately.
From the performance point of view, depending on the scenario, it can be beneficial to increase the minimal console log level and keep the more detailed data in the log file.

To set the ERROR log level for a file backend, type::

  (machine-0) logLevel 2 file

Peripherals can also have different log levels on different backends::

  (machine-0) logLevel 1 file sysbus.uart

Logging access to peripherals
-----------------------------

Apart from the regular logger configuration, you can enable logging of accesses to specific peripherals.
This feature is enabled only for peripherals registered on a system bus.

To enable it, run::

    (machine-0) sysbus LogPeripheralAccess sysbus.uart

Now, whenever the CPU tries to read or write to this peripheral, you will see a message similar to this one::

    14:32:28.6083 [INFO] uart: ReadByte from 0x0 (TransmitData), returned 0x0.

To enable logging access to all peripherals, run::

    (machine-0) sysbus LogAllPeripheralsAccesses true

Creating a trace of the execution
'''''''''''''''''''''''''''''''''

It is possible to create a trace of every function executed by the binary::

    (machine-0) sysbus.cpu LogFunctionNames true

As a result the names of the functions will be printed to the log at ``INFO`` level::

    17:05:23.8834 [INFO] cpu: Entering function kobject_uevent_env at 0xC014CD9C
    17:05:23.8834 [INFO] cpu: Entering function dev_uevent_name (entry) at 0xC018FA5C
    17:05:23.8834 [INFO] cpu: Entering function dev_uevent_name at 0xC018FA70
    17:05:23.8834 [INFO] cpu: Entering function kobject_uevent_env at 0xC014CDA8
    17:05:23.8835 [INFO] cpu: Entering function kobject_uevent_env at 0xC014CDB8
    17:05:23.8835 [INFO] cpu: Entering function kmem_cache_alloc (entry) at 0xC0085610
    17:05:23.8835 [INFO] cpu: Entering function kmem_cache_alloc at 0xC0085630

If you are interested only in a subset of functions, you can limit the results by providing space-separated names prefixes::

    (machine-0) sysbus.cpu LogFunctionNames true "dev kobject"

You can also avoid logging subsequent duplicate function names by adding another ``true`` argument either instead or after the optional function name prefixes::

    (machine-0) sysbus.cpu LogFunctionNames true ["dev kobject"] true

Only such three lines would remain printed in the aforementioned example with both function name filtering and duplicate removal applied::

    17:05:23.8834 [INFO] cpu: Entering function kobject_uevent_env at 0xC014CD9C
    17:05:23.8834 [INFO] cpu: Entering function dev_uevent_name (entry) at 0xC018FA5C
    17:05:23.8834 [INFO] cpu: Entering function kobject_uevent_env at 0xC014CDA8

Hushing excessive unhandled access logs
---------------------------------------

Renode, by default, informs you about unhandled accesses to memory ranges that are not covered by any model.
You may see logs like this::

    09:21:8.1960 [WARNING] sysbus: [cpu: 0x08001200] WriteDoubleWord to non existing peripheral at 0x400D0114, value 0xFFFFFFFF.
    09:21:9.4538 [WARNING] sysbus: [cpu: 0x080012E6] ReadDoubleWord from non existing peripheral at 0x400D0118, returning 0x0.

These logs are there to inform you that your platform's description is not complete and if you observe issues with your simulation it might be one of the possible cases.

Very often these unhandled regions will not affect any important aspects of the execution and you might want to silence these logs.

While changing the :ref:`log-level` to ``ERROR`` to hide warnings might be one option, it could be a too radical solution as you might want to continue seeing other warnings. 

The best way to achieve fine-grained logging control in this case is with the ``SilenceRange`` feature.
E.g. if you want to disable logging for addresses in the range between ``0x80000`` and ``0x801000``, run::

    sysbus SilenceRange <0x80000 0x1000>

You can do it from the REPL level in the ``sysbus`` init section as well::

    sysbus:
        init:
            SilenceRange <0x80000 0x1000>
