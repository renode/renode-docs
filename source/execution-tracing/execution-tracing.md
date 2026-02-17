# Execution tracing in Renode

Renode has complete awareness of the internal state of all simulated components and can use this information to trace the execution of unmodified binaries without any behavioral changes to the simulation.

```{note}
Some logging features may significantly impact the simulation's performance, but they do not affect the execution itself.
```

```{note}
Commands listed below assume that you have a platform loaded, a CPU node named `cpu` and that the `using sysbus` command was executed.
For more details, see documentation chapters on [Renode Script syntax](renode-script-syntax) and [Accessing and manipulating peripherals](accessing-and-manipulating-peripherals).
```

## Logging executed function names

Renode can log the names of functions currently executed by the guest application.
This requires you to use the `sysbus LoadELF @path/to/elf` command to [load your application](../basic/machines.md#loading-binaries) or `sysbus LoadSymbolsFrom @path/to/elf` if you prefer executing a binary or a hex file.
Function name logging can be enabled using:

```none
cpu LogFunctionNames true
```

You can disable function name logging using:

```none
cpu LogFunctionNames false
```

```{note}
You can also add another `true` at the end of this command to remove duplicate function names from subsequent code blocks and achieve better overall performance.
```

To filter function names based on a prefix, add the prefix as a string at the end of the function:

```none
cpu LogFunctionNames true "uart"
```

To use more than one prefix and log functions that start with either of these two prefixes, simply separate them with a space:

```none
cpu LogFunctionNames true "uart irq"
```

```{note}
Renode will try to demangle C++ function names.
It will also use the names stored in the ELF file.
```

If you want to learn more about logging executed function names in Renode, visit the [Using the logger chapter](../basic/logger.md)

## Logging peripheral accesses

While the information about the executed functions gives you an overall understanding of the execution, it is often beneficial to know the additional context and understand why the application took a specific path.

To provide this additional context, Renode can log access to peripherals.
This feature allows you to see how your program uses or doesn't use specific parts of the SoC.

You can enable this feature by using the following:

```none
sysbus LogPeripheralAccess <peripheral-name> true
```

```{note}
In most cases, your peripheral names need a prefix `sysbus` like `sysbus.uart0`.
You can omit this prefix if you're using the `using sysbus` command in your script.
```

The logs contain:

- the name of the peripheral
- current value of the program counter
- type and width of the access
- offset of the access (relative to the peripheral's base address) and the name of the register that this offset maps to
- the value that was either loaded to or returned from the register

You can also log accesses to all peripherals connected to the system bus:

```none
sysbus LogAllPeripheralsAccess true
```

You can disable both peripheral access logging commands by providing `false` instead of `true` as the last parameter:

```none
sysbus LogAllPeripheralsAccess false
```

If you want to learn more about logging peripheral accesses in Renode, visit the [Using the logger chapter](../basic/logger.md)

## Execution tracing

In Renode, you can see what the CPU does at any given time without changing the code or using specialized hardware.
To enable execution tracing, use:

```none
cpu CreateExecutionTracing "tracer_name" @path-to-file <mode>
```

You can use the tracer to track additional data. To do so, type:

```none
tracer_name <tracker_name>
```

where `tracker_name` can be one of the following:

- `TrackMemoryAccesses` - tracks memory accesses.
- `TrackVectorConfiguration` - tracks vector configuration for the RISC-V architecture.

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

```none
cpu CreateExecutionTracing "tracer_name" @path-to-file <mode> true
```

If you also want to compress the output, you can add another `true` to this command:

```none
cpu CreateExecutionTracing "tracer_name" @path-to-file <mode> true true
```

You can view the content of the binary file by using a script bundled with Renode.
It can be invoked by running this command in your shell:

```sh
python3 <renode>/tools/execution_tracer/execution_tracer_reader.py inspect path-to-dump-file
```

This command will print the file's text content to the standard output.

To disable execution tracing, simply use:

```none
cpu DisableExecutionTracing
```

## Usage of gathered data

Certain tools shipped with Renode can use the obtained execution traces for post-mortem analysis of a program's execution.
These include:
* the [Coverage Report Generator](./coverage-report.md) which can be used to generate code coverage reports,
* the [Guest CPU Cache Modelling tool](./guest-cache-modelling.md) which simulates CPU caches and generates usage statistics.

## Specialized uses of execution tracing

In addition to generic program execution tracing, Renode also has more specialized tracing-related facilities, such as:
* [counting executed opcodes](./metrics-and-profiling.md#opcode-counting)
* [generating interactive flamegraphs of the guest's execution trace](./metrics-and-profiling.md#guest-application-profiling)
* [obtaining execution metrics](../basic/metrics.md)

Refer to the [Execution metrics, profiling and opcode counting](./metrics-and-profiling.md) section for more details.
