.. _verilator-cosimulation:

Co-simulating HDL models
========================

Renode has introduced an integration layer for Verilator - a well known, fast and open source HDL simulator which lets you use hardware implementations written in Verilog within a Renode simulation.

Integration layer
-----------------

The `integration layer <https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin/VerilatorIntegrationLibrary/src>`_ has been implemented as a plugin for Renode and consists of two parts: C# classes, which manage the Verilator simulation process, and an integration library written in C++, which allows you to turn your Verilog hardware models into a Renode 'verilated' peripheral.

The 'verilated' peripheral is compiled separately and the resulting binary is started by Renode.
The interprocess communication is based on sockets.

Creating a 'verilated' peripheral
---------------------------------

Example 'verilated' models are available on `Antmicro’s GitHub <https://github.com/antmicro/renode-verilator-integration>`_.

To make your own 'verilated' peripheral, in the main cpp file of your 'verilated' model you need to include C++ headers applicable to the bus you are connecting to, and the type of external interfaces you want to integrate with Renode - e.g. UART’s rx/tx signals.

.. code-block:: cpp

    // uart.h and axilite.h can be found in Renode's VerilatorPlugin
    #include "src/peripherals/uart.h"
    #include "src/buses/axilite.h"

Next, you will need to define a function that will call your model’s eval function, and provide it as a callback to the integration library structure, along with bus and peripheral signals.

.. code-block:: cpp

    void eval() {
    #if VM_TRACE
    main_time++;
    tfp->dump(main_time);
    #endif
    top->eval();
    }

    void Init() {
    AxiLite* bus = new AxiLite();

    //==========================================
    // Init bus signals
    //==========================================
    bus->clk = &top->clk;
    bus->rst = &top->rst;
    bus->awaddr = (unsigned long *)&top->awaddr;
    bus->awvalid = &top->awvalid;
    bus->awready = &top->awready;
    bus->wdata = (unsigned long *)&top->wdata;
    bus->wstrb = &top->wstrb;
    bus->wvalid = &top->wvalid;
    bus->wready = &top->wready;
    bus->bresp = &top->bresp;
    bus->bvalid = &top->bvalid;
    bus->bready = &top->bready;
    bus->araddr = (unsigned long *)&top->araddr;
    bus->arvalid = &top->arvalid;
    bus->arready = &top->arready;
    bus->rdata = (unsigned long *)&top->rdata;
    bus->rresp = &top->rresp;
    bus->rvalid = &top->rvalid;
    bus->rready = &top->rready;

    //==========================================
    // Init eval function
    //==========================================
    bus->evaluateModel = &eval;

    //==========================================
    // Init peripheral
    //==========================================
    uart = new UART(bus, &top->txd, &top->rxd,
    prescaler);
    }

As part of the last step, in the ``main`` function, you have to call ``simulate``, providing it with port numbers, which are passed as the first two command-line arguments of the resulting binary.

.. code-block:: cpp

    Init();
    uart->simulate(atoi(argv[1]), atoi(argv[2]));

This project uses the `ZeroMQ <https://zeromq.org>`_ messaging library that you need to install in your system.

Now you can compile your project with Verilator::

    verilator -LDFLAGS "-lzmq -lpthread" -cc top.v --exe -CFLAGS "-Wpedantic -Wall -I$(INTEGRATION_DIR)" sim_main.cpp $(INTEGRATION_DIR)/src/renode.cpp $(INTEGRATION_DIR)/src/buses/axilite.cpp $(INTEGRATION_DIR)/src/peripherals/uart.cpp

    make -j 4 -C obj_dir -f Vtop.mk

The resulting simulation can be attached to the Renode platform and used in a .repl file as a 'verilated' peripheral.

.. code-block::

    uart: Verilated.VerilatedUART @ sysbus <0x70000000, +0x100>
        simulationFilePath: "verilated_simulation_file_path"
        frequency: 100000000


Core-v-mcu "Hello World" example with 'verilated' UART
------------------------------------------------------

Prepare the binary
++++++++++++++++++

Instructions how to setup SDK are available on `pulp-builder repository <https://github.com/pulp-platform/pulp-builder/tree/arnold>`_.
After configuration, set ``PULPRT_HOME`` environment variable with the path to the ``pulp-rules`` directory.

You also need to edit the SDK source code.
To write a character to the ``txd`` UART register, add in ``__rt_putc_uart`` function in `io.c file <https://github.com/pulp-platform/pulp-rt/blob/eaf528a1926b9e12f94e4aa66e3f5768263db678/libs/io/io.c>`_:

.. code-block:: cpp

    *((volatile uint32_t*)(0x50000004)) = c;

The "Hello World" code source can be found on `pulp-rt-examples <https://github.com/pulp-platform/pulp-rt-examples/tree/master/hello>`_.
To compile, run::

    make all io=uart

The resulting binary should be created in the ``pulp-rt-examples/hello/build/arnold/test`` directory.

Run in the Renode simulation
++++++++++++++++++++++++++++

To enable a 'verilated' UART peripheral in the core-v-mcu hello world example, you need to register ``VerilatedUART`` in `core-v-mcu.repl <https://github.com/renode/renode/blob/master/platforms/cpus/core-v-mcu.repl>`_, e.g.::

    verilated_uart: Verilated.VerilatedUART @ sysbus <0x50000000, +0x100>
        frequency: 100000000

Then, you have to provide a binary to the Renode simulation in the Renode monitor type::

    (monitor) using sysbus
    (monitor) mach create
    (machine-0) machine LoadPlatformDescription @platforms/cpus/core-v-mcu.repl

Attach your binary to the simulation::

    (machine-0) sysbus LoadELF @path_to_your_binary

You can use your 'verilated' UART model::

    (machine-0) verilated_uart SimulationFilePath @path_to_verilated_uart_model

Or you can use the prebuilt one provided by us::

    (machine-0) $uart?=@https://dl.antmicro.com/projects/renode/verilator--uartlite_trace_off-s_252704-c703fe4dec057a9cbc391a0a750fe9f5777d8a74
    (machine-0) verilated_uart SimulationFilePath $uart

To enable the UART analyzer window and start simulation, type::

    (machine-0) showAnalyzer verilated_uart
    (machine-0) s

Verilator Trace
---------------

You can also enable signal trace dumping by setting the ``VERILATOR_TRACE=1`` variable in the shell in which you compile the 'verilated' model.
The resulting trace is written into a vcd file and can be viewed in e.g. `GTKWave viewer <http://gtkwave.sourceforge.net/>`_.

.. image:: img/gtkwave-trace.png
