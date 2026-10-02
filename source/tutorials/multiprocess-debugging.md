# Debugging multiple binaries at once in GDB

Renode supports debugging heterogenous multiprocessor setups via GDB's multiprocess extension and multiple inferiors.
This tutorial showcases an example flow and various options that can be used based on the i.MX 8M Plus platform running Linux with a [Coral NPU](https://github.com/google-coral/coralnpu) accelarator.

Additonal information about multiprocess debugging can be found in [GDB's documentation](https://sourceware.org/gdb/current/onlinedocs/gdb.html/index.html), especially in chapters:
* [Debugging Multiple Inferiors Connections and Programs](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Inferiors-Connections-and-Programs.html#Inferiors-Connections-and-Programs)
* [Stopping and Starting Multi-thread Programs](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Thread-Stops.html#Thread-Stops)

## Prerequisites

* Recent version of Renode. As of Renode 1.17.0, multiprocess debugging is not available in a tagged version of Renode, so you can either:
  * Download nightly package from [builds.renode.io](https://builds.renode.io/).
  * Built Renode [from source](../advanced/building_from_sources.md).
* GDB client compiled with support for the `aarch64` and `riscv:rv32` targets, as well as support for the multiprocess extension. For example, `gdb-multiarch`, available in various Linux distributions.
* U-Boot binary that will be loaded into GDB, which can be downloaded from: https://dl.antmicro.com/projects/renode/u-boot-s_10073016-b1b07345dc1a11114194b13057c6d2884793bbfe.
* Copy of the U-Boot sources used by the demo, which can be cloned from GitHub:
```bash
git clone https://github.com/nxp-imx/uboot-imx --branch lf_v2025.04 --depth 1
```

## Setting up the platform in Renode

Start Renode and load the demo script from the Monitor window by running:

```none
(monitor) i @scripts/complex/coral_npu/imx8mplus_linux_coral.resc
```

Then, start the multiprocess GDB server in Renode by running:

```none
(frdm_imx8mp_npu) machine StartMultiprocessGdbServer 3333 [ca53Cluster, CoralNPU_RVV]
```

This will start the server on port `3333` with two processes defined:
* Process 1 - containing the Cortex-A cluster
* Process 2 - containing the Coral NPU

## Setting up in GDB

Start the GDB clinet and connect to the port on which the GDB server has been started in Renode, using the `extended-remote` mode:

```none
(gdb) target extended-remote :3333
Remote debugging using :3333
```

GDB should automatically connect to Process 1, which can be verified by running the `info threads` command and observing that all four processors are visible:

```none
(gdb) info threads
  Id   Target Id                         Frame
* 1    Thread 1.1 "frdm_imx8mp_npu.cpu0" 0x0000000000970000 in ?? ()
  2    Thread 1.2 "frdm_imx8mp_npu.cpu1" 0x0000000000970000 in ?? ()
  3    Thread 1.3 "frdm_imx8mp_npu.cpu2" 0x0000000000970000 in ?? ()
  4    Thread 1.4 "frdm_imx8mp_npu.cpu3" 0x0000000000970000 in ?? ()
```

Load the U-Boot symbol file into GDB using the `symbol-file` command, and add the directory with the cloned U-Boot sources:

```none
(gdb) symbol-file u-boot-s_10073016-b1b07345dc1a11114194b13057c6d2884793bbfe
Reading symbols from u-boot-s_10073016-b1b07345dc1a11114194b13057c6d2884793bbfe...

(gdb) dir uboot-imx/
Source directories searched: /home/user/uboot-imx:$cdir:$cwd
```

Next, create another inferior in GDB. From it, attach to the Coral NPU process:

```none
(gdb) add-inferior
[New inferior 2]
Added inferior 2 on connection 1 (extended-remote :3333)

(gdb) inferior 2
[Switching to inferior 2 [<null>] (<noexec>)]

(gdb) attach 2
Attaching to process 2
```

The output of the `info threads` command should now show all five CPUs:

```none
(gdb) info threads
  Id   Target Id                                 Frame
  1.1  Thread 1.1 "frdm_imx8mp_npu.cpu0"         0x0000000000970000 in ?? ()
  1.2  Thread 1.2 "frdm_imx8mp_npu.cpu1"         0x0000000000970000 in ?? ()
  1.3  Thread 1.3 "frdm_imx8mp_npu.cpu2"         0x0000000000970000 in ?? ()
  1.4  Thread 1.4 "frdm_imx8mp_npu.cpu3"         0x0000000000970000 in ?? ()
* 2.1  Thread 2.5 "frdm_imx8mp_npu.CoralNPU_RVV" 0x00000000 in ?? ()
```

:::{note}
GDB should automatically detect the architecture of the connected processes - there should be no need to set it manually.
:::

Finally, switch GDB's focus back to the Cortex-A cluster using the `inferior` command:

```none
(gdb) inferior 1
[Switching to inferior 1 [process 1] (<noexec>)]
[Switching to thread 1.1 (Thread 1.1)]
```

## Debugging the Cortex-A cluster

Create a breakpoint on U-Boot's entry point and start the emulation to reach it:

```none
(gdb) b _main
Breakpoint 1 at 0x402b3930: file arch/arm/lib/crt0_64.S, line 85.

(gdb) c
Continuing.

Thread 1.1 "frdm_imx8mp_npu.cpu0" hit Breakpoint 1, _main () at arch/arm/lib/crt0_64.S:85
85		ldr	x0, =(SYS_INIT_SP_ADDR)
(gdb)
```

From there, you can add additional breakpoints and debug the U-Boot binary using the usual GDB commands, e.g., `step`, `stepi`, `next`, `continue`.
You can also inspect the state of the emulated processors using the usual commands, e.g., `info registers`, `info threads`.

After completing the debugging process, run `continue` in GDB and observe the boot process in Renode's `uart2` window:

```none
...
[    4.146200] fec 30be0000.ethernet: clk_ptp clock rate is zero
[    4.160500] fec 30be0000.ethernet: Invalid MAC address: 00:00:00:00:00:00
[    4.162500] fec 30be0000.ethernet: fec clock (0) too fast to get right mii speed
[    4.165000] fec 30be0000.ethernet: probe with driver fec failed with error -22

==== Hello World! Linux i.MX 8M Plus ====

#
```

## Debugging the Coral NPU

Load the test binary into the NPU from the emulated Linux guest by running the following command in Renode's `uart2` window:

```none
# prepare_coral
coral: staging 832 bytes...
  832/832 bytes (100%)
coral: program staged
#
```

Start the Coral NPU from the Linux guest by using the `run_coral` command:

```none
# run_coral
```

You may notice that the NPU has not started executing instructions.
By default, GDB will only resume processors which belong to the currently active inferior.
As we are currently connected to inferior 1 (the Cortex-A cluster), the Coral NPU will remain paused.

To start executing the payload, send the interrupt signal from GDB by pressing `Ctrl-C`. This will interrupt the emulation. After it stops, switch to inferior 2 to start debugging the program loaded to the NPU:

```none
^C
Thread 1.1 "frdm_imx8mp_npu.cpu0" received signal SIGINT, Interrupt.
0xffff800080fff508 in ?? ()

(gdb) inferior 2
[Switching to inferior 2 [process 2] (<noexec>)]
[Switching to thread 2.1 (Thread 2.5)]
#0  0x00000000 in ?? ()
```

Now you can debug the execution of the program loaded into the NPU using the usual GDB mechanisms, such as:

```none
(gdb) stepi
0x00000008 in ?? ()
(gdb) x/i $pc
=> 0x8:	csrr	a0,minstret
```

:::{note}
While focused on inferior 2, none of the CPUs connected to inferior 1 (the Cortex-A cluster) will be executing instructions.
:::

After completing the debugging process, run `continue` in GDB to let the NPU finish executing the loaded program and pause itself:

```none
(gdb) continue
Continuing.

Thread 2.1 "frdm_imx8mp_npu.CoralNPU_RVV" received signal SIGINT, Interrupt.
0x00000140 in ?? ()
```

In Renode's logs, you should see that the Coral NPU stopped due to executing the `mpause` instruction:

```none
[INFO] CoralNPU_RVV: MPAUSE executed
```

You can switch back to inferior 1 and `continue` to resume the Linux guest:

```none
(gdb) inferior 1
[Switching to inferior 1 [process 1] (<noexec>)]
[Switching to thread 1.1 (Thread 1.1)]
#0  0xffff800080fff508 in ?? ()

(gdb) c
Continuing.
```

After that, you should see that the Linux guest observed that the NPU has finished executing the program and displayed the result on the `uart2` window:

```none
coral: finished, output[0] = 0x0007
#
```

## Running all inferiors at once

While the previous section described a flow of debugging where only one inferior is running at a time, it is also possible to instruct GDB to resume all inferiors at once using the `schedule-multiple` option.

Interrupt the emulation from GDB by sending the interrupt signal by pressing `Ctrl-C`:

```none
^C
Thread 1.1 "frdm_imx8mp_npu.cpu0" received signal SIGINT, Interrupt.
0xffff800080fff508 in ?? ()
```

Enable GDB to run multiple inferiors at once using the `set schedule-multiple on` command:

```none
(gdb) set schedule-multiple on
```

Swich to inferior 2 and add a breakpoint on address `0x0`, which will be the first address executed by the NPU:

```none
(gdb) inferior 2
[Switching to inferior 2 [process 2] (<noexec>)]
[Switching to thread 2.1 (Thread 2.5)]
#0  0x00000140 in ?? ()

(gdb) b *0x0
Breakpoint 2 at 0x0
```

Switch back to inferior 1 and `continue` the emulation for GDB:

```none
(gdb) inferior 1
[Switching to inferior 1 [process 1] (<noexec>)]
[Switching to thread 1.1 (Thread 1.1)]
#0  0xffff800080fff508 in ?? ()

(gdb) continue
Continuing.
```

On the `uart2` window of the emulated Linux guest window, run the Coral NPU once more using the `run_coral` command:

```none
# run_coral
```

You should see that GDB recognized that the NPU started executing instructions and triggered a breakpoint on address `0x0`, automatically switching its focus to the NPU's inferior:

```none
Continuing.
[Switching to Thread 2.5]

Thread 2.1 "frdm_imx8mp_npu.CoralNPU_RVV" hit Breakpoint 2, 0x00000000 in ?? ()

(gdb) inferior
[Current inferior is 2 [process 2] (<noexec>)]
```

:::{note}
Renode follows the [All-Stop Mode](https://sourceware.org/gdb/current/onlinedocs/gdb.html/All_002dStop-Mode.html#All_002dStop-Mode) semantics, meaning that while GDB is allowed to resume multiple inferiors at once, a stop condition on any of them (e.g., hitting a breakpoint) will cause all other inferiors to pause execution as well.
:::

:::{note}
Note that with `schedule-multiple` enabled, GDB may resume the other inferiors while single-stepping on the currently focused inferior.
The setting can be changed freely while the emulation is paused using:

```none
set schedule-multiple on
```

to enable and:

```none
set schedule-multiple off
```

to disable.
:::

In GDB, use `continue` to let the Coral NPU finish its program.
This should once again pause the emulation as a result of the `mpause` instruction:

```none
(gdb) c
Continuing.

Thread 2.1 "frdm_imx8mp_npu.CoralNPU_RVV" received signal SIGINT, Interrupt.
0x00000140 in ?? ()
```

Since `schedule-multiple` is enabled, after another `continue` in GDB, you should immediately see the result of the NPU program on the `uart2` window:

```none
coral: finished, output[0] = 0x0007
#
```
