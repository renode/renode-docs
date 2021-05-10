.. _verilator-cosimulation:

Co-simulating HDL models
========================

Renode includes an integration layer for `Verilator <https://veripool.org/verilator/>`_ - a well known, fast and open source HDL simulator which lets you use hardware implementations written in Verilog within a Renode simulation.

This tutorial can be run on Linux and Windows operating systems.

Integration layer
-----------------

The integration layer has been implemented as a plugin for Renode and consists of two parts: `C# classes <https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin>`_, which manage the Verilator simulation process, and `an integration library written in C++ <https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin/VerilatorIntegrationLibrary>`_, which allows you to turn your Verilog hardware models into a 'verilated' Renode peripheral.

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

As part of the last step, in the ``main`` function, you have to call ``simulate`` with two port numbers on which Renode awaits communication.

These port numbers are passed as command-line arguments when Renode starts the 'verilated' peripheral.

.. code-block:: cpp

   Init();
   uart->simulate(atoi(argv[1]), atoi(argv[2]));

Building a 'verilated' peripheral
---------------------------------

There are a few prerequisites:

* a local copy of `the renode-verilator-integration repository <https://github.com/antmicro/renode-verilator-integration>`_,
* a local copy of `the Renode repository <https://github.com/renode/renode>`_ because of its `VerilatorIntegrationLibrary <https://github.com/renode/renode/tree/master/src/Plugins/VerilatorPlugin/VerilatorIntegrationLibrary>`_,
* Verilator >= v4.024.

``$RVI_PATH``, ``$RENODE_PATH`` and ``$VERILATOR_PATH``, respectively, will be used to refer to the paths of these three prerequisites.
The path to Verilator won't be needed if it's properly installed, i.e., the executable is available in ``PATH`` and the ``verilator-config.cmake`` can be found according to the `CMake's find_package search procedure <https://cmake.org/cmake/help/latest/command/find_package.html#search-procedure>`_.

The path to the directory containing Verilog and C/C++ source files will be referred to as ``$SRC_PATH``.
It's best to place that directory directly in the ``renode-verilator-integration`` repository root.
Such placement ensures correctness of the default path to the `configure-and-verilate.cmake <https://github.com/antmicro/renode-verilator-integration/blob/master/cmake/configure-and-verilate.cmake>`_ file that contains the CMake logic common to all peripherals.

.. note::

   To be able to run shell commands without any modifications, set all ``*_PATH`` shell variables prior to running the commands.

Preparing the peripheral directory
++++++++++++++++++++++++++++++++++

First, put all Verilog and C/C++ source files in ``$SRC_PATH``.
Then, copy the ``$RVI_PATH/cmake/CMakeLists.txt.template`` as ``CMakeLists.txt`` to the ``$SRC_PATH`` directory::

   # Execute from a directory containing peripheral's source files
   mkdir "$SRC_PATH"
   cp *.v *.c *.cpp "$SRC_PATH"
   cp "$RVI_PATH/cmake/CMakeLists.txt.template" "$SRC_PATH/CMakeLists.txt"

The project's ``$SRC_PATH/CMakeLists.txt`` file needs minor adjustments to work well with a specific peripheral (only the first two are required):

* replace ``<PROJECT_NAME>`` with a chosen name,
* replace ``<MODULE_FILES>`` and ``<C_SRC_FILES>`` with paths to the peripheral files relative to the ``$SRC_PATH``,
* add chosen arguments to be always used during a certain phase of the build by removing ``#`` and replacing ``<ARGS>`` with actual arguments in lines that set the ``COMP_ARGS``, ``LINK_ARGS`` and ``VERI_ARGS`` variables,
* if the peripheral's source directory isn't placed directly in ``<RVI_PATH>``, then adjust the path to ``configure-and-verilate.cmake`` in the ``include`` command.

.. note::

   Use a space to separate multiple files or arguments replacing ``<*_FILES>`` and ``<ARGS>`` placeholders.

Build commands
++++++++++++++

Having the CMake source directory prepared, the 'verilated' peripheral can now be built.
When using CMake, it's best to keep the build files in a separate build directory::

   mkdir build && cd build
   cmake -DCMAKE_BUILD_TYPE=Release -DUSER_RENODE_DIR="$RENODE_PATH" ${VERILATOR_PATH:+"-DUSER_VERILATOR_DIR=$VERILATOR_PATH"} "$SRC_PATH"
   make

If the build succeeds, ``Vtop`` is the built 'verilated' peripheral.

.. note::

   ``RENODE_ROOT`` and ``VERILATOR_ROOT`` environment variables can be used instead of CMake ``USER_RENODE_DIR`` and ``USER_VERILATOR_DIR`` variables (respectively).
   In case both environment and CMake variables are specified for Renode or Verilator, CMake variables have higher priority.

.. note::

   Use `make -j $(nproc)` (`make -j $(sysctl -n hw.logicalcpu)` on macOS) to optimize build speed by creating as many jobs as the number of available CPU cores.

Linux-specific build information
++++++++++++++++++++++++++++++++

On Linux, it is advised to use OpenLibm to enable running 'verilated' peripherals with older GNU libc versions.
This is because a few common mathematical functions have been recently updated in the GNU libm (which is a part of GNU libc).
If the peripheral is linked against them, these updated functions will also be needed to run the peripheral.

To use it, pass an additional ``-DLIBOPENLIBM=$RVI_PATH/lib/libopenlibm-Linux-x86_64.a`` argument to the ``cmake`` command to use the OpenLibm library that is currently also used by Renode.

Windows-specific build information
++++++++++++++++++++++++++++++++++

The aforementioned steps with a few minor changes were tested to successfully build peripherals on Windows with `Cygwin <https://www.cygwin.com/>`_ and `MSYS2 <https://www.msys2.org/>`_.
MSYS2 has a well-supported `mingw-w64-verilator <https://packages.msys2.org/base/mingw-w64-verilator>`_ package, so it doesn't require building Verilator.

.. note::

   On Windows it's even more important to use absolute paths.
   These could be Cygwin/MSYS2 absolute paths, i.e. ``/home/<...>``.
   Both Windows and Unix path styles are supported.

The CMake command from the `Build commands`_ section requires adding these arguments to work on Windows with Cygwin/MSYS2 and MinGW:

* ``-G "MinGW Makefiles"`` – to generate a ``Makefile`` for ``MinGW make``,
* ``-DCMAKE_SH=CMAKE_SH-NOTFOUND`` – required for CMake to work on Windows despite having ``sh.exe`` in ``PATH``.

Additionally, in the most common toolchain setups, the ``mingw32-make`` command should be used instead of ``make`` even if both are available.

Therefore, on Windows a 'verilated' peripheral can be built with::

   cmake -G "MinGW Makefiles" -DCMAKE_SH=CMAKE_SH-NOTFOUND -DCMAKE_BUILD_TYPE=Release -DUSER_RENODE_DIR="$RENODE_PATH" ${VERILATOR_PATH:+"-DUSER_VERILATOR_DIR=$VERILATOR_PATH"} "$SRC_PATH"
   mingw32-make

Running a 'verilated' peripheral
--------------------------------

After building a 'verilated' executable it's time to attach it to a :ref:`Renode machine <working-with-machines>` so that it is actually used as a peripheral.

First, a dedicated peripheral has to be added to a :ref:`Renode platform description (.repl) file <describing-platforms>` that is going to be used to configure the machine.
For a 'verilated' UART peripheral called e.g. ``myVerilatedPeripheral``, add these lines into your ``.repl`` file::

   myVerilatedPeripheral: Verilated.VerilatedUART @ sysbus <0x70000000, +0x100>
       frequency: 100000000

.. note::

   The ``Verilated.BaseDoubleWordVerilatedPeripheral`` type should be used instead of ``Verilated.VerilatedUART`` for 'verilated' peripherals other than UART.

In Renode, after loading such a platform description with a command either directly in the :ref:`Renode monitor <monitor>` or with an appropriate :ref:`Renode script (.resc) file <scripts>`, the 'verilated' executable needs to be attached.
Assuming the ``Vtop`` executable is located in the Renode root directory, it can be attached with::

   (machine-0) myVerilatedPeripheral SimulationFilePath @Vtop

Otherwise, an absolute path or a path relative to the Renode root directory can be used instead of ``Vtop``.

.. note::

   Note that paths have to start with the ``@`` symbol or be surrounded by double quotes ``"``.

Core-v-mcu "Hello World" example with 'verilated' UART
------------------------------------------------------

Prepare the binary
++++++++++++++++++

Instructions how to setup the SDK are available on the `pulp-builder repository <https://github.com/pulp-platform/pulp-builder/tree/arnold>`_.
After configuration, set the ``PULPRT_HOME`` environment variable with a path to the ``pulp-rules`` directory.

You also need to edit the SDK source code.
To write a character to the ``txd`` UART register, add in ``__rt_putc_uart`` function in `io.c file <https://github.com/pulp-platform/pulp-rt/blob/eaf528a1926b9e12f94e4aa66e3f5768263db678/libs/io/io.c>`_:

.. code-block:: cpp

   *((volatile uint32_t*)(0x50000004)) = c;

The "Hello World" code source can be found at `pulp-rt-examples <https://github.com/pulp-platform/pulp-rt-examples/tree/master/hello>`_.
To compile, run::

   make all io=uart

The resulting binary should be created in the ``pulp-rt-examples/hello/build/arnold/test`` directory.

Run in Renode simulation
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
