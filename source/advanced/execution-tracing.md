# Execution tracing in Renode

Renode has complete awareness of the internal state of all simulated components and can use this information to trace the execution of unmodified binaries without any behavioral changes to the simulation.

```{note}
Some logging features may significantly impact the simulation's performance, but it does not affect the execution itself.
```

```{note}
Commands listed below assume that you have a platform loaded, a CPU node named `cpu` and that the `using sysbus` command was executed.
For more details see documentation chapters on [Renode Script syntax](renode-script-syntax) and [Accessing and manipulating peripherals](accessing-and-manipulating-peripherals).
```

## Logging executed function names

Renode can log the names of functions currently executed by the guest application.
This requires you to use the `sysbus LoadELF @path/to/elf` command to [load your application](https://renode.readthedocs.io/en/latest/basic/machines.html#loading-binaries) or `sysbus LoadSymbolsFrom @path/to/elf` if you prefer executing a binary or a hex file.
Function names logging can be enabled using:

```
cpu LogFunctionNames true
```

You can disable function names logging using:

```
cpu LogFunctionNames false
```

```{note}
You can also add another `true` at the end of this command to remove duplicate function names from subsequent code blocks and achieve better overall performance.
```

To filter function names based on a prefix, add the prefix as a string at the end of the function:

```
cpu LogFunctionNames true "uart"
```

To use more than one prefix and log functions that start with either of those two prefixes, simply separate them with a space:

```
cpu LogFunctionNames true "uart irq"
```

```{note}
Renode will try to demangle C++ function names.
It will also use the names stored in the ELF file.
```

If you want to learn more about logging executed function names in Renode, visit [Using the logger chapter](https://renode.readthedocs.io/en/latest/basic/logger.html)

## Logging peripheral accesses

While executed functions information gives you an overall understanding of the execution, it is often beneficial to know the additional context and understand why the application took a specific path.

To provide this additional context, Renode can log access to peripherals.
This feature allows you to see how your program uses or doesn't use specific parts of the SoC.

You can enable this feature by using the following:

```
sysbus LogPeripheralAccess <peripheral-name> true
```

```{note}
In most cases, your peripheral names need a prefix `sysbus` like `sysbus.uart0`.
You can omit this prefix if you use the `using sysbus` command in your script.
```

The logs contain:
- the name of the peripheral,
- current value of the program counter,
- type and width of the access,
- offset of the access (relative to the peripheral's base address) and the name of the register that this offset maps to,
- the value that was either loaded to or returned from the register.

You can also log accesses to all peripherals connected to the system bus:

```
sysbus LogAllPeripheralsAccess true
```

You can disable both peripheral access logging commands by providing `false` instead of `true` as the last parameter:

```
sysbus LogAllPeripheralsAccess false
```

If you want to learn more about logging peripheral accesses in Renode, visit [Using the logger chapter](https://renode.readthedocs.io/en/latest/basic/logger.html)

## Execution tracing

In Renode, you can see what the CPU does at any given time without changing the code or using specialized hardware.
To enable execution tracing, use:

```
cpu EnableExecutionTracing @path-to-file <mode>
```

`mode` can be one of the following values:
- `PC` - this mode saves all program counter values.
Example:

```
0x20400000
0x20400004
0x20400008
0x2040000c
0x20401bc4
0x20401bc8
...
```
- `Opcode` - this mode saves all executed opcodes.
Example:

```
0x0297
0x1028293
0x30529073
0x3B90106F
0x5FC00297
0x88C28293
...
```
- `PCAndOpcode` - this mode saves program counter values and the corresponding opcode that was executed.
Example:

```
0x20400000: 0x0297
0x20400004: 0x1028293
0x20400008: 0x30529073
0x2040000c: 0x3B90106F
0x20401bc4: 0x5FC00297
0x20401bc8: 0x88C28293
...
```
- `Disassembly` - in addition to the value of the program counter and the corresponding opcode, this mode uses a built-in LLVM-based disassembler to convert opcodes to human-readable instruction names with all of the used arguments.
The output also includes the name of the symbol that this entry belongs to.
Example:

```
0x20400000:   00000297  auipc t0, 0           [vinit (entry)]
0x20400004:   01028293  addi t0, t0, 16       [vinit+0x4 (guessed)]
0x20400008:   30529073  csrw mtvec, t0        [vinit+0x8 (guessed)]
0x2040000c:   3b90106f  j 7096                [vinit+0xC (guessed)]
0x20401bc4:   5fc00297  auipc t0, 392192      [__start (entry)]
0x20401bc8:   88c28293  addi t0, t0, -1908    [__start+0x4 (guessed)]
...
```

You can save the output from the `PC`, `Opcode`, and `PCAndOpcode` modes to a binary format that can optionally be compressed.
This format is faster to encode and produces smaller output files.
To save to a binary file, use the following:

```
cpu EnableExecutionTracing @path-to-file <mode> true
```

If you also want to compress the output, you can add another `true` to this command:

```
cpu EnableExecutionTracing @path-to-file <mode> true true
```

You can view the content of the binary file by using a script bundled with Renode.
It can be invoked by running this command in your shell:

```
python3 <renode>/tools/execution_tracer/execution_tracer_reader.py path-to-dump-file
```

This command will print the file's text content to the standard output.

To disable execution tracing, simply use:

```
cpu DisableExecutionTracing
```

## Execution metrics

Renode can gather and show you a few different metrics in the form of graphs.
The metrics that are available out of the box are: 
* Executed instructions,
* Exceptions,
* Memory access,
* Peripheral access.

If you want to learn more about this feature and see it in action, visit the [Metrics analyzer chapter](https://renode.readthedocs.io/en/latest/basic/metrics.html).

## Guest application profiling

In Renode, you can display a trace of the guest application's execution in the form of an interactive flame graph.
You can use this to visualize the flow of the application, analyze the relative time taken by each function, and discover potential issues with the implemented functionality or its performance.

```{note}
This feature is available on RISC-V, Cortex-A, and Cortex-M CPUs.
```

To enable guest profiling, use:

```
cpu EnableProfiler <output-format> @path-to-output-file [<flush-instantly>]
```

Currently, Renode supports two output formats:
- `CollapsedStack` - a text-based, collapsed stack format that can be viewed interactively using [speedscope](https://www.speedscope.app/)
- `Perfetto` - a binary format that can be viewed using [Perfetto](https://ui.perfetto.dev/)

You can also use `cpu EnableProfilerCollapsedStack` and `cpu EnableProfilerPerfetto` commands for the same effect.

By default, Renode will buffer file operations for better performance, but you can instantly write everything to a file by passing `true` as the optional `<flush-instantly>` argument.
If you don't want to write to a file instantly but still want to have some control over when a flush occurs, use the following command to flush the buffer manually:

```
cpu FlushProfiler
```

You can inspect traces generated from Zephyr samples in [Renodepedia](https://antmicro.com/blog/2022/08/renodepedia/) - see the examples for [RISC-V](https://zephyr-dashboard.renode.io/renodepedia/boards/hifive1/?view=software&demo=Hello_World) and [Cortex-M](https://zephyr-dashboard.renode.io/renodepedia/boards/stm32f103_mini/?view=software&demo=Hello_World). 

## Opcode counting

Renode can count how many times a specific instruction was executed.
This can be helpful if you want to know if some special instructions, for example, vector instructions, are executed in your program.

To enable opcode counting, use the following command:

```
cpu EnableOpcodesCounting true
```

After that, you must install a pattern of the opcode you want to trace.

Opcode patterns have to be built from the following characters:
* `1` matches set bits,
* `0` matches unset bits,
* all other characters match any value.

They are like a regex that matches the opcode’s bits.
As an example, you can use the [scripts/single-node/versatile.resc](https://github.com/renode/renode/blob/master/scripts/single-node/versatile.resc) demo to detect ARM’s branch and branch-with-link instructions.
To load this demo, use:

```
include @scripts/single-node/versatile.resc
```

To install the counter patterns, we will use these two commands, but you can search for any pattern you want:

```
cpu InstallOpcodeCounterPattern "bl" "****1011************************"
cpu InstallOpcodeCounterPattern "b"  "****1010************************"
```

To get the values of the counters printed to the monitor window, use:

```
cpu GetAllOpcodesCounters
```

The first parameter is the name of the counter, and the second is the pattern.
After running the demo, you can use:

```
----------------
|Opcode|Count  |
----------------
|bl    |376816 |
|b     |9587263|
----------------
```

You can also get the value of a specified counter using:

```
cpu GetOpcodeCounter "<counter-name>"
```

### Installing RISC-V opcode patterns

Renode offers predefined functions for RISC-V to install the patterns for you.
To install RISC-V specific opcode patterns, use the functions below:

- `cpu EnableRiscvOpcodesCounting` - to install patterns for general instructions,
- `cpu EnableCustomOpcodesCounting` - to install patterns for custom RISC-V instructions,
- `cpu EnableVectorOpcodesCounting` - to install patterns for RISC-V vector instructions.

All those patterns are created from RISC-V opcode definition [files](https://github.com/renode/renode-infrastructure/tree/master/src/Emulator/Cores/RiscV/opcodes).
You can create a similar file for RISC-V with your instructions and load the patterns using:

```
cpu EnableRiscvOpcodesCounting @path-to-file
```

