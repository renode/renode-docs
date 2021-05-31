.. _basic-control:

Basic execution control
=======================

Renode allows you to precisely control the execution of the emulation.

Starting and pausing the execution
----------------------------------

At the beginning emulation is in *paused* state which means that no machine is running and *virtual time* is not progressing.

To start the emulation execute::

    (machine-0) start
    Starting emulation...

To pause it type::

    (machine-0) pause
    Pausing emulation...

Executing instruction-by-instruction
------------------------------------

When you need to analyze in details how the execution of your binary influences the state of a hardware you can switch to *stepping* execution mode::

    (machine-0) sysbus.cpu ExecutionMode SingleStepBlocking

This will stop the emulation after execution of each instruction. In order to move to the next one type::

    (machine-0) sysbus.cpu Step

When you want to return to the *normal* execution mode type::

    (machine-0) sysbus.cpu ExecutionMode Continuous

More advance control can be obtained by connecting external GDB.

Blocking and non-blocking stepping
----------------------------------

When you use ``SingleStepBlocking`` mode the emulation won't progress between steps.
This can cause problems with blocking the emulation when executing multiple cores instruction-by-instruction, in which case ``SingleStepNonBlocking`` mode is the preferred option.
The drawback of the non-blocking mode is that the virtual time will progress between steps, which might introduce desynchronization and timeout-related issues.

The ``Step`` command will preserve the current mode when in instruction-by-instruction flow and use the default value (``SingleStepBlocking``) otherwise.
This behavior can be overridden by selecting the non-blocking mode explicitly::

    (machine-0) sysbus.cpu Step false

Inspecting current location
---------------------------

Renode allows you to easily examine the current state of your application::

    (machine-0) sysbus.cpu PC
    0xC01890A8

As a result you will get a hexadecimal address of the instruction currently executed.

If you want to know the name of the function that is currently executed (assuming your binary has been compiled with the symbols inside) type::

    (machine-0) sysbus FindSymbolAt `sysbus.cpu PC` # equivalent of 0xC01890A8
    uart_console_write

This will print the name of the symbol.
