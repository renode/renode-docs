(basic-control)=

# Basic execution control

Renode allows you to precisely control the execution of the emulation.

## Starting and pausing the execution

In the beginning the emulation is in a *paused* state, which means that no machine is running and *virtual time* is not progressing.

To start the emulation, execute:

```
(machine-0) start
Starting emulation...
```

To pause it, type:

```
(machine-0) pause
Pausing emulation...
```

## Executing instruction-by-instruction

```{note}
Although using Renode's native stepping is a viable solution, we recommend using [GDB](https://www.sourceware.org/gdb/) to perform step-by-step execution.
Using GDB with Renode emulated machines is described in detail in the {ref}`documentation chapter devoted to this issue<gdb-debugging>`.

More information on how step execution in GDB can be found in the [GDB documentation](https://sourceware.org/gdb/download/onlinedocs/gdb/Continuing-and-Stepping.html).
```

When you need to analyze in detail how the execution of your binary influences the state of the hardware, you can switch to the *stepping* execution mode:

```
(machine-0) sysbus.cpu ExecutionMode SingleStepBlocking
```

This will stop the emulation after the execution of each instruction. In order to move to the next one, type:

```
(machine-0) sysbus.cpu Step
```

When you want to return to the *normal* execution mode, type:

```
(machine-0) sysbus.cpu ExecutionMode Continuous
```

More advanced control can be obtained by connecting an external GDB.

## Blocking and non-blocking stepping

When you use `SingleStepBlocking` mode, the emulation won't progress between steps.
This can cause problems with blocking the emulation when executing multiple cores instruction-by-instruction, in which case `SingleStepNonBlocking` mode is the preferred option.
The drawback of the non-blocking mode is that the virtual time will progress between steps, which might introduce desynchronization and timeout-related issues.

The `Step` command will preserve the current mode when in instruction-by-instruction flow and use the default value (`SingleStepBlocking`) otherwise.
This behavior can be overridden by selecting the non-blocking mode explicitly:

```
(machine-0) sysbus.cpu Step false
```

## Inspecting the current location

Renode allows you to easily examine the current state of your application:

```
(machine-0) sysbus.cpu PC
0xC01890A8
```

As a result, you will get the hexadecimal address of the instruction currently being executed.

If you want to know the name of the function that is currently being executed (assuming your binary has been compiled with the symbols inside) type:

```
(machine-0) sysbus FindSymbolAt `sysbus.cpu PC` # equivalent of 0xC01890A8
uart_console_write
```

This will print the name of the symbol.
