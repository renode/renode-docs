# Co-simulating with Verilator

Renode includes an integration layer for [Verilator](https://veripool.org/verilator/) - a well-known, fast, and open source HDL simulator that lets you use hardware implementations written in Verilog within a Renode simulation.

You can connect your verilated peripherals with interrupts and external interfaces, like UART Rx/Tx lines.

## Integration layer

The integration layer has been implemented as a plugin for Renode. It consists of two parts: [C# classes](https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin), which manage the Verilator simulation process, and [an integration library written in C++](https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin/VerilatorIntegrationLibrary), which allows you to turn your Verilog hardware models into a verilated Renode peripheral.

The verilated peripheral is compiled separately, and the resulting binary is started by Renode.
The interprocess communication is based on sockets.
Alternatively, you can compile the verilated block as a library and communicate via library calls.

## Supported buses

Verilator co-simulation in Renode supports the following buses:

* APB3
* AXI4
* AXI4Lite
* Wishbone
* CFU Custom Function Unit interface

## Using pre-compiled HDL models

Shipping with Renode are several `.resc` files that use pre-compiled HDL models, corresponding to the sources in the [renode-verilator-integration repository](https://github.com/antmicro/renode-verilator-integration).

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

## Building your own verilated peripheral models

You can find many examples of verilated peripherals models like CFU, UART, RAM, and even a CPU in the [renode-verilator-integration repository](https://github.com/antmicro/renode-verilator-integration).

Visit the {doc}`../tutorials/co-simulating-custom-hdl` chapter for detailed instructions how to build the peripherals from that repository or your own verilated peripheral models.