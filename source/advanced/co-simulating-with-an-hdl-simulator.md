# Co-simulating with an HDL simulator

Renode includes two integration methods for HDL co-simulation, allowing you to connect HDL peripherals with interrupts and external interfaces, like UART Rx/Tx lines:

* DPI-based SystemVerilog method (for simulators supporting DPI like Verilator, Questa or VCS)
* Custom [Verilator](https://www.veripool.org/verilator/)-only C++ method

## Adding co-simulated blocks

The Renode side of the integration layer is a plugin called CoSimulationPlugin, consisting of [C# classes](https://github.com/renode/renode/tree/master/src/Plugins/CoSimulationPlugin), which initiate the communication.

Typically an instance of the `CoSimulatedPeripheral` class corresponds to an HDL model.
To add a co-simulated block to your platform, use the following snippet in your [REPL file](https://renode.readthedocs.io/en/latest/basic/describing_platforms.html#describing-platforms):

```none
block: CoSimulated.CoSimulatedPeripheral @ sysbus <0x20000000, +0x100000>
```

## DPI-based integration method

In this case, messages between Renode and an HDL simulator are transmitted over TCP sockets using the standard DPI interface supported in many simulators, including Verilator, VCS or Questa.

As the DPI layer relies on a TCP socket connection, you need to also specify the `address` parameter for the peripheral:

```none
block: CoSimulated.CoSimulatedPeripheral @ sysbus <0x20000000, +0x100000>
    address: "127.0.0.1"
```

The HDL side uses a [SystemVerilog interface](https://github.com/renode/renode/tree/master/src/Plugins/CoSimulationPlugin/IntegrationLibrary/hdl) which connects directly to your HDL simulation using signals specific to the bus you are simulating.

For co-simulation, you can pass the external simulator location via the `SimulationPath` property to spawn it automatically by Renode.
In such case you can pass custom command line parameters using the `SimulationContext` property, e.g. for Verilator:

```none
block: CoSimulated.CoSimulatedPeripheral @ sysbus <0x20000000, +0x100000>
    address: "127.0.0.1"
    SimulationPath: build/verilated
    SimulationContext: "--custom_features_enabled +RENODE_RECEIVER_PORT={0} +RENODE_SENDER_PORT={1} +RENODE_ADDRESS={2}"
```

Otherwise, the HDL simulator has to be running before connecting to it.

### Supported buses

* AHB
* APB3
* AXI4
* AXI4-Lite

### Examples

You can find examples for every supported bus with instructions on building them in the [renode-dpi-examples repository](https://github.com/antmicro/renode-dpi-examples).
All examples have been tested both with [Verilator](https://www.veripool.org/verilator/) and [Questa](https://www.intel.com/content/www/us/en/software/programmable/quartus-prime/questa-edition.html).

## Custom, direct integration metod (Verilator-only)

When using Verilator, you can also compile your HDL simulation as a dynamic library and link it with Renode at runtime, instead of using TCP sockets.
Renode can spawn or link a simulation on its own.

```{note}
You shouldn't specify the `address` parameter for a peripheral that is connected as a dynamic library.
```

To interface your HDL simulation with Renode you need to connect signals of your HDL design with a [C++ interface](https://github.com/renode/renode/tree/master/src/Plugins/CoSimulationPlugin/IntegrationLibrary/src).

### Supported buses

* APB3
* AXI4
* AXI4-Lite
* Wishbone
* CFU Custom Function Unit interface

### Examples

You can find many examples of verilated peripheral models such as [CFU](https://github.com/antmicro/renode-verilator-integration/tree/master/samples/cfu_basic), [UART](https://github.com/antmicro/renode-verilator-integration/tree/master/samples/uartlite), [RAM](https://github.com/antmicro/renode-verilator-integration/tree/master/samples/ram), and even a [CPU](https://github.com/antmicro/renode-verilator-integration/tree/master/samples/cpu_ibex) in the [renode-verilator-integration repository](https://github.com/antmicro/renode-verilator-integration).
For detailed instructions on how to build models from the repository or your own, see {doc}`../tutorials/co-simulating-custom-hdl`.

## Connecting to verilated models

When using Verilator, your HDL models are first translated to C++ (or 'verilated') and then compiled.

Renode comes with several `.resc` files that use HDL models precompiled in this way (we also sometimes call them 'verilated' in their compiled form, to explain their origin), like a [verilated UART model](https://github.com/renode/renode/blob/master/scripts/single-node/riscv_verilated_liteuart.resc) or [verilated Ibex](https://github.com/renode/renode/blob/master/scripts/single-node/verilated_ibex.resc).

The Monitor command used to load the verilated model library depends on your host OS.
On Linux, to add a precompiled FastVDMA HDL model to a peripheral named `dma`, you would run:

```none
dma SimulationFilePathLinux @https://dl.antmicro.com/projects/renode/zynq-fastvdma_libVfastvdma-Linux-x86_64-1246779523.so-s_2057616-93e755f7d67bc4d5ca33cce6c88bbe8ea8b3bd31
```

You you can use `SimulationFilePathLinux`, `SimulationFilePathMacOS`, and `SimulationFilePathWindows` in the same script if you want to provide different payloads for different OSes, making the script multi-platform.
Renode will select the one that matches your host OS.

If you are interested in just a single operating system, you can simply use `SimulationFilePath` and Renode will interpret it as a model matching your current OS.

By convention, we host two types of precompiled models:
* models prefixed with `V` use the socket based integration
* models prefixed with `libV` communicate with Renode via library calls

Most of the built-in scripts use binaries with the `libV` prefix.
