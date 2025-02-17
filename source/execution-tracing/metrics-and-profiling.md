# Execution metrics, profiling and opcode counting

Renode lets you tailor the execution tracking functionality to meet specific needs in terms of metrics, profiling and opcode counting.

## Execution metrics

Renode can gather and show you metrics in the form of graphs.
The metrics that are available out of the box are:

* Executed instructions
* Exceptions
* Memory access
* Peripheral access

If you want to learn more about this feature and see it in action, visit the [Metrics analyzer chapter](../basic/metrics.md).

## Guest application profiling

In Renode, you can display a trace of the guest application's execution in the form of an interactive flame graph.
You can use this to visualize the flow of the application, analyze the relative time taken by each function, and discover potential issues with the implemented functionality or its performance.

```{note}
This feature is available for RISC-V, Cortex-A, Cortex-R and Cortex-M CPUs.
```

To enable guest profiling, use:

```none
cpu EnableProfiler <output-format> @path-to-output-file [<flush-instantly>]
```

Renode supports two output formats:

* `CollapsedStack` - a text-based, collapsed stack format that can be viewed interactively using [speedscope](https://www.speedscope.app/)
* `Perfetto` - a binary format that can be viewed using [Perfetto](https://ui.perfetto.dev/)

You can also use the `cpu EnableProfilerCollapsedStack` and `cpu EnableProfilerPerfetto` commands for the same effect.

By default, Renode will buffer file operations for better performance, but you can instantly write everything to a file by passing `true` as the optional `<flush-instantly>` argument.
If you don't want to write to a file instantly but still want to have some control over when a flush occurs, use the following command to flush the buffer manually:

```none
cpu FlushProfiler
```

You can inspect traces generated from Zephyr samples in the [System Designer](https://designer.antmicro.com/) platform - see examples for [RISC-V](https://designer.antmicro.com/hardware/devices/hifive1) and [Cortex-M](https://designer.antmicro.com/hardware/devices/stm32f103_mini).

## Opcode counting

Renode can count how many times a specific instruction was executed.
This can be helpful if you want to know if some special instructions, for example, vector instructions, are executed in your program.

To enable opcode counting, use the following command:

```none
cpu EnableOpcodesCounting true
```

Then, you need to install a pattern of the opcode you want to trace.

Opcode patterns have to be built from the following characters:

* `1` matches set bits
* `0` matches unset bits
* all other characters match any value

The patterns resemble a regex that matches the opcode’s bits.
As an example, you can use the [scripts/single-node/versatile.resc](https://github.com/renode/renode/blob/master/scripts/single-node/versatile.resc) demo to detect ARM’s branch and branch-with-link instructions.
To load this demo, use:

```none
include @scripts/single-node/versatile.resc
```

To install the counter patterns, this example uses the following two commands, but you can search for any pattern you want:

```none
cpu InstallOpcodeCounterPattern "bl" "****1011************************"
cpu InstallOpcodeCounterPattern "b"  "****1010************************"
```

To print the values of the counters to the Monitor window, use:

```none
cpu GetAllOpcodesCounters
```

The first parameter is the name of the counter, and the second is the pattern.
After running the demo, you can use:

```none
----------------
|Opcode|Count  |
----------------
|bl    |376816 |
|b     |9587263|
----------------
```

You can also get the value of a specified counter using:

```none
cpu GetOpcodeCounter "<counter-name>"
```

### Installing RISC-V opcode patterns

Renode offers predefined functions for RISC-V to install the patterns for you.
To install RISC-V specific opcode patterns, use the functions below:

* `cpu EnableRiscvOpcodesCounting` - to install patterns for general instructions
* `cpu EnableCustomOpcodesCounting` - to install patterns for custom RISC-V instructions
* `cpu EnableVectorOpcodesCounting` - to install patterns for RISC-V vector instructions

These patterns are created from RISC-V opcode definition [files](https://github.com/renode/renode-infrastructure/tree/master/src/Emulator/Cores/RiscV/opcodes).
You can create a similar file for RISC-V with your instructions and load the patterns using:

```none
cpu EnableRiscvOpcodesCounting @path-to-file
```
