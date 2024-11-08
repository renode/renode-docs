# Loading assembly to memory

Renode allows the user to load assembly code in several ways:

* [LLVMAssembler](https://github.com/renode/renode/blob/791eec59cc66650893c0ff5dd3dc2909b7229bd5/tests/unit-tests/arm-ge-flag.robot#L25) used mainly for tests,
* {rsrc}`writing hex instructions directly <tests/unit-tests/riscv-custom-instructions.robot#L140>` which can be used for custom instructions,
* loading compiled ASM code directly, described below

```{note}
Before going further, it is recommended to read the [Debugging with GDB](https://renode.readthedocs.io/en/latest/debugging/gdb.html)
and [Debugging with VSCode](https://renode.readthedocs.io/en/latest/debugging/vscode.html) chapters.
```

## Prerequisites

You need to have the target architecture's GNU toolchain, e.g [RISC-V](https://github.com/riscv-collab/riscv-gnu-toolchain) or [ARM](https://developer.arm.com/Tools%20and%20Software/GNU%20Toolchain). We'll use `riscv64-unknown-elf-*` utilities (for ARM you'd use `arm-none-eabi-*`).


## Compiling assembly code to an executable

Let's start with simple RISC-V assembly that stores and loads from memory at `0x00064000`:

```asm
.globl _start
_start:
    li a0, 0x00064000
    li a2, 0x5
    sw zero, (a0)
    lw a4, (a0)
    sw a2, (a0)
    lw a4, (a0)
loop:
    j loop
```

To compile the code use your GNU toolchain's `as` and `ld`:

```
riscv64-unknown-elf-as -march=rv64imac_zba_zbb asm.s -o asm.o
riscv64-unknown-elf-ld asm.o -o asm.elf
```

Let's use this simple asm.resc file with platform:
```
using sysbus
machine LoadPlatformDescriptionFromString
"""
cpu: CPU.RiscV64 @ sysbus
    cpuType: "rv64imac_zba_zbb"
    privilegedArchitecture: PrivilegedArchitecture.Priv1_10
    timeProvider: empty

dram: Memory.MappedMemory @ sysbus 0x00
    size: 0x06400000
"""
machine StartGdbServer 3333
sysbus LoadELF @asm.elf
```

Notice, that we need CPU type and model in our platform to match compiled ASM code. Here we have model `CPU.RiscV64` and `cpuType` as `rv64imac_zba_zbb`.
For more details go to [Configuring a RISC-V CPU](https://renode.readthedocs.io/en/latest/basic/configuring-a-risc-v-cpu.html).

Start Renode with this .resc file:

```
$ renode asm.resc
(monitor) i $CWD/test.resc
(machine-0) 
```

Now in separate terminal use the target architecture's GDB:

```
$ riscv64-unknown-elf-gdb asm.elf
```

In GDB connect to Renode's GDB server:

```
(gdb) target remote :3333
Remote debugging using :3333
0x00000000000100b0 in _start ()
```

It's best to use GDB's TUI with ASM and register view. To do that:

```
(gdb) tui enable
(gdb) layout asm
(gdb) layout regs
```

Now you can see registers and our assembly source. 
To step over use `si`.

```
┌─Register group: general────────────────────────────────────────────────────────────────────────────────────┐
│zero           0x0      0                             ra             0x0      0x0                           │
│sp             0x0      0x0                           gp             0x0      0x0                           │
│tp             0x0      0x0                           t0             0x0      0                             │
│t1             0x0      0                             t2             0x0      0                             │
│fp             0x0      0x0                           s1             0x0      0                             │
│a0             0x0      0                             a1             0x0      0                             │
│a2             0x0      0                             a3             0x0      0                             │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
│  >0x100b0 <_start>        lui     a0,0x64                                                                  │
│   0x100b4 <_start+4>      li      a2,5                                                                     │
│   0x100b6 <_start+6>      sw      zero,0(a0)                                                               │
│   0x100ba <_start+10>     lw      a4,0(a0)                                                                 │
│   0x100bc <_start+12>     sw      a2,0(a0)                                                                 │
│   0x100be <_start+14>     lw      a4,0(a0)                                                                 │
│   0x100c0 <loop>          j       0x100c0 <loop>                                                           │
│   0x100c2                 unimp                                                                            │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
remote Thread 1 (asm) In: _start                                                            L??   PC: 0x100b0 
(gdb) 
```

Do note that some instructions are pseudoinstructions and
the source you've written may not necessarily be the same as the assembly view in GDB.
The generated instructions may also differ between LLVMAssembler and GNU as.

## Debugging tlib

```{note}
Remember to compile and start Renode with debug flag (`build.sh -d`, `renode -d`) for this to work!
```

Renode also gives you option to see how the instructions are being translated. To do that we'll use VSCode.

After starting Renode and attaching GDB, move to VSCode and navigate to `src/Infrastructure/src/Emulator/Cores/tlib/arch/riscv/translate.c`
and set the breakpoint right before the `case OPC_RISC_LUI:`, and use the provided `(gdb) Tlib Attach` launch script.

Search for the Renode process, it should be `mono` or `dotnet` type, attach to it (you may need to elevate your privileges to root, for
rootless debugging check [YAMA's ptrace_scope](https://www.kernel.org/doc/html/latest/admin-guide/LSM/Yama.html#ptrace-scope)). 

Then do `si` in GDB, which should make your VSCode stop at the previously-set breakpoint.