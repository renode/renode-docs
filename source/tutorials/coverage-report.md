# Generating a coverage report

Renode offers many execution tracing features, as described in the [Execution tracing](https://renode.readthedocs.io/en/latest/advanced/execution-tracing.html#execution-tracing) section, and allows you to dump the entire execution of a binary into a single file. 
With an execution trace of a properly built binary and a dedicated script it's possible to create a code coverage report.
[The script](https://github.com/renode/renode/blob/master/tools/execution_tracer/execution_tracer_reader.py) combines data in [the DWARF format](https://dwarfstd.org/) (debug information available in ELF files, which are typically used to load software to Renode) with the number of executions of each instruction counted by Renode. 
The following tutorial will walk you through the steps necessary to generate such a report in Renode.

## Prerequisites

To generate a report, you need to have Renode installed along with [the execution tracer script](https://github.com/renode/renode/blob/master/tools/execution_tracer/execution_tracer_reader.py).
On Linux you can simply download a portable package by following [these instructions](https://github.com/renode/renode/blob/master/README.md#using-the-linux-portable-release).

It's assumed that you execute the rest of commands in the directory of the Renode package, otherwise you need to change the path to the appropriate installation location.

To run the script you need to first install the prerequisites:
```
python3 -m pip install -r tools/execution_tracer/requirements.txt
```

## Building a binary

Renode can trace execution of a binary built in any way, but the script requires a binary with debug information in the DWARF format.
To provide the best result it's recommended to use the `-g` and `-Og` flags (for GCC) during compilation.
Please note that different compilers may require different options.

The `-g` switch adds debug information to the binary, specifically code line numbers for each machine instruction.
The script requires that information, so the lack of it causes an error. 

The `-Og` switch disables most optimizations and is intended to make the debugging process easier.
Any optimization done by a compiler may prevent some redundant lines of code from being executed.
For the purpose of generating a coverage report, same as for debugging, it's recommended to execute the code without any optimizations.
Generating a report for an optimized binary may create imprecise or even unexpected results.

For the purpose of this tutorial we've prepared [example code](https://dl.antmicro.com/projects/renode/coverage-tests/main.c) and [a prebuilt binary](https://dl.antmicro.com/projects/renode/coverage-tests/coverage-test.elf-s_3603888-0f7cfe992528c2576a9ac6a4dcc3a41b03d1d6eb).
You can easily download them using the following commands:
```bash
wget https://dl.antmicro.com/projects/renode/coverage-tests/main.c
wget -O main.elf https://dl.antmicro.com/projects/renode/coverage-tests/coverage-test.elf-s_3603888-0f7cfe992528c2576a9ac6a4dcc3a41b03d1d6eb 
```

## Tracing execution

To trace execution of the binary from the previous section, you can simply use the RESC script below.
You can also execute these commands manually in Monitor.
```{note}
The script runs the binary prebuilt for the Kendryte K210 platform, but the mechanism is generic and works for all platforms.
```
```
$bin=$CWD/main.elf
include @scripts/single-node/kendryte_k210.resc

cpu1 CreateExecutionTracing "trace" $CWD/trace.bin.gz PC True True

emulation RunFor "0.017" # Run 1.7 million instructions (default performance is 100MIPS)
quit
```
The crucial command is the one that initializes execution tracing, specifically `CreateExecutionTracing`.
The [Execution tracing](https://renode.readthedocs.io/en/latest/advanced/execution-tracing.html#execution-tracing) section contains details on configuring the command.
The script that generates the coverage report requires at least PCs (addresses of executed instructions) in the trace file.
```{note}
Tracing an additional type of data may cause an increase in the size of the output file.
It's also recommended to use a binary format and compression by setting the fourth and fifth arguments to `True`, as shown above.
```

## Generating the report

Finally, you can run the script that generates the report:
```bash
tools/execution_tracer/execution_tracer_reader.py coverage trace.bin.gz --binary main.elf --sources main.c --output main.c.cov
```
 
The output file (`main.c.cov`) should start with the lines shown below.
The number before the colon indicates the number of executions of each line.
```
    0:  #include <stdio.h
    0:	#include "bsp.h"
    0:	
    0:	const int buf_size = 100;
    0:	
   28:	void funB(int *buf, int b) {
 2828:		for (int i = 0; i < buf_size; i++) {
 2800:			buf[i] -= b;
    0:		}
   28:	}
    0:	
```

```{note}
If no sources are provided using `--sources` argument, the script will attempt to automatically discover their locations based on the DWARF data extracted from the binary.

It might be needed to perform path substitution if the sources' locations changed from the time when the binary was built (or binaries were built on a different machine).

For this `--sub-source-path` argument can be used, by providing `old_path:new_path` for each pair of paths to be substituted; this argument can be provided multiple times.
```

It's possible for the script to output data in LCOV-compatible format (*.info) by using `--lcov-format` switch.
