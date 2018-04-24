.. _basic-control:

Basic control
.............

Renode allows you to precisely control the execution of the emulation.

Starting and pausing the execution
''''''''''''''''''''''''''''''''''

At the beginning emulation is in *paused* state which means that no machine is running and *virtual time* is not progressing.

To start the emulation execute::

    (machine-0) start
    Starting emulation...

To pause it type::

    (machine-0) pause
    Pausing emulation...

Executing instruction-by-instruction
''''''''''''''''''''''''''''''''''''

When you need to analyze in details how the execution of your binary influences the state of a hardware you can switch to *stepping* execution mode::

    (machine-0) sysbus.cpu ExecutionMode SingleStep

This will stop the emulation after execution of each instruction. In order to move to the next one type::

    (machine-0) sysbus.cpu Step

When you want to return to the *normal* execution mode type::

    (machine-0) sysbus.cpu ExecutionMode Continuous

More advance control can be obtained by connecting external GDB.

Inspecting current location
'''''''''''''''''''''''''''

Renode allows you to easily examine the current state of your application::

    (machine-0) sysbus.cpu PC
    0xC01890A8

As a result you will get a hexadecimal address of the instruction currently executed.

If you want to know the name of the function that is currently executed (assuming your binary has been compiled with the symbols inside) type::

    (machine-0) sysbus FindSymbolAt `sysbus.cpu PC` # equivalent of 0xC01890A8
    uart_console_write

This will print the name of the name of the symbol.
