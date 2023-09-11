# Co-simulating with a HDL simulator

Renode includes an integration layer for HDL simulators.
It allows you to connect an HDL peripheral with interrupts and external interfaces, like UART Rx/Tx lines.

Thanks to the integration using SystemVerilog DPI, Renode can co-simulate with virtually any HDL simulator that supports Direct Programming Interface. 
If you are using [Verilator](https://veripool.org/verilator/), you can use DPI or a [custom integration layer](https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin/VerilatorIntegrationLibrary/src).

## Integration layer

The protocol that transfers messages between Renode and an HDL simulator uses TCP sockets.
When using Verilator, you can also use direct function calls from dynamically linked binaries.

Renode side of the integration layer plugin consists of [C# classes](https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin), which initiate communication and spawn simulator process when needed.

The HDL side can use one of two interfaces:
* [SystemVerilog interface](https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin/VerilatorIntegrationLibrary/hdl) - which connects directly to your HDL simulation, using only signals
* [C++ interface](https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin/VerilatorIntegrationLibrary/src) - which requires the use of a simulation with a main loop written in C++.

```{note}
For Verilator, you should use the C++ interface.
```

## Supported buses

Co-simulation in Renode supports the following buses:

* APB3
* AXI4
* AXI4-Lite

Verilator integration also supports the following features:

* Wishbone bus
* CFU Custom Function Unit interface

## Using pre-compiled HDL models

To use an HDL model in Renode simulation, you need to compile it first.
Renode comes with several `.resc` files that use pre-compiled HDL models, like [Verilated Ibex](https://github.com/renode/renode/blob/master/scripts/single-node/verilated_ibex.resc).
For more Verilog models, see the [renode-verilator-integration repository](https://github.com/antmicro/renode-verilator-integration).

A script containing a verilated peripheral like [riscv_verilated_liteuart.resc](https://github.com/renode/renode/blob/master/scripts/single-node/riscv_verilated_liteuart.resc) can be loaded and started like any other script, by running e.g.:

```
start @path/to/your/script.resc
```

````{note}
The Monitor command which is used in those scripts to load the verilated peripheral model differs slightly depending on your OS.
On Linux, to add a FastVDMA HDL model named to peripheral named `dma`, you would run:

```
dma SimulationFilePathLinux @https://dl.antmicro.com/projects/renode/zynq-fastvdma_libVfastvdma-Linux-x86_64-1246779523.so-s_2057616-93e755f7d67bc4d5ca33cce6c88bbe8ea8b3bd31
```

You you can use `SimulationFilePathLinux`, `SimulationFilePathMacOS`, and `SimulationFilePathWindows` in the same script if you want to provide different payloads for different OSes.
Renode will select the one that matches your host OS.

If you are interested in just a single operating system, you can simply use `SimulationFilePath` and Renode will interpret it as a model matching your current OS.
````

There are two types of precompiled models:
* Models prefixed with `V` use the socket based integration
* Models prefixed with `libV` communicate with Renode via library calls

Most of the built-in scripts use binaries with the `libV` prefix.

Renode chooses the communication mechanism based on the peripheral's `address` parameter, which is usually set in a REPL file.
If `address` is specified, your peripheral will use socket-based communication, otherwise it will use library calls.

## Building your own verilated peripheral models

You can find many examples of verilated peripheral models such as [CFU](https://github.com/antmicro/renode-verilator-integration/tree/master/samples/cfu_basic), [UART](https://github.com/antmicro/renode-verilator-integration/tree/master/samples/uartlite), [RAM](https://github.com/antmicro/renode-verilator-integration/tree/master/samples/ram), and even a [CPU](https://github.com/antmicro/renode-verilator-integration/tree/master/samples/cpu_ibex) in the [renode-verilator-integration repository](https://github.com/antmicro/renode-verilator-integration).
For detailed instructions on how to build models from the repository or your own, see {doc}`../tutorials/co-simulating-custom-hdl`.

To use an HDL simulator other than Verilator, such as [Questa](https://www.intel.com/content/www/us/en/software/programmable/quartus-prime/questa-edition.html), follow the instructions in the [renode-dpi-examples repository](https://github.com/antmicro/renode-dpi-examples).

Both repositories contain CMake files that work on Linux and Windows.
