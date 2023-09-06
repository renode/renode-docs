# Co-simulating with a HDL simulator

Renode includes an integration layer for HDL simulators.
It allows you to connect your peripheral written in a HDL with interrupts and external interfaces, like UART Rx/Tx lines.

Thanks to the integration using SystemVerilog DPI, Renode can co-simulate with virtually any HDL simulator which supports Direct Programming Interface. 
Instead of using the DPI based integration you can use another one dedicated for [Verilator](https://veripool.org/verilator/) (an open-source and fast HDL simulator).

## Integration layer

There is a dedicated protocol which transfers messages between Renode and simulator using one of two available mechanisms:
* TCP sockets 
* by direct calls of functions from dynamically linked binary

The integration layer, available as a plugin for Renode, consists of two parts.
The Renode side consists of [C# classes](https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin), which initiates communication and spawn simulator process if needed.

The opposite side can use socket connection and one of the following interfaces written in:
* [SystemVerilog](https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin/VerilatorIntegrationLibrary/hdl) - which connects to your HDL simulation directly, just by signals
* [C++](https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin/VerilatorIntegrationLibrary/src) - which requires usage of a simulation with a main loop written in C++

The second one interface interacts well with Verilator.
Same as the third option, a C++ interface with a communication using calls of functions available in a dynamically linked library, which essentially is a HDL simulation.

## Supported buses

Co-simulation in Renode supports the following buses:

* APB3
* AXI4
* AXI4-Lite

The integration dedicated for Verilator supports also the following features:

* Wishbone bus
* CFU Custom Function Unit interface

## Using pre-compiled HDL models

The HDL simulation is compiled separately. 
Renode come with several `.resc` files that use pre-compiled HDL models, corresponding to the sources in the [renode-verilator-integration repository](https://github.com/antmicro/renode-verilator-integration).

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

You you can use `SimulationFilePathLinux`, `SimulationFilePathMacOS`, and `SimulationFilePathWindows` in the same script;
Renode will select the one that matches your host OS.
````

There are two types of pre-compiled models.
One with the prefix `V` uses the socket based integration and the another with the name starting with `libV` communicates with Renode via library calls.
Most of shipped scripts use binaries with the `libV` prefix.

Renode chooses communication mechanism based on appearance of the `address` parameter of peripheral, required for socket based communication.
It's typically set in a REPL file.

## Building your own verilated peripheral models

You can find many examples of verilated peripherals models like CFU, UART, RAM, and even a CPU in the [renode-verilator-integration repository](https://github.com/antmicro/renode-verilator-integration).
Visit the {doc}`../tutorials/co-simulating-custom-hdl` chapter for detailed instructions how to build the peripherals from that repository or your own verilated peripheral models.

If you need to use simulator different than Verilator, in example [Questa](https://www.intel.com/content/www/us/en/software/programmable/quartus-prime/questa-edition.html), you can build your co-simulation following the instruction from the [renode-dpi-examples repository](https://github.com/antmicro/renode-dpi-examples).

Both repositories contains CMake files which works on Linux and Windows. 


