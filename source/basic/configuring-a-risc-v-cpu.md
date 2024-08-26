# Configuring a RISC-V CPU

Among the architectures supported in Renode, RISC-V is one of the most prominent.
Renode supports both 32 and 64-bit versions of RISC-V, Privileged Architecture in various versions and a broad range of extensions.

The most common base ISA sets supported by Renode are:

- RV32/64I Base (`I`)
- Integer Multiplication and Division (`M`)
- Atomic Instructions (`A`)
- Single-Precision Floating-Point (`F`)
- Double-Precision Floating-Point (`D`)
- Control and Status Register Instructions (`Zicsr`)
- Instruction-Fetch Fence (`Zifencei`)

All of the above constitute the `G` set.

Renode also supports many of the ISA extensions like:

- Compressed Instructions (`C`)
- Vector Operations (`V`)
- Bit-manipulation
  - Address generation instructions (`Zba`)
  - Basic bit-manipulation (`Zbb`)
  - Carry-less multiplication (`Zbc`)
  - Single-bit instructions (`Zbs`)
- Half-Precision Floating-Point (`Zfh`)

Lastly, Renode also supports custom, non standard instruction sets.
Some of them can be selected like other instruction sets(e.g. `Xandes`), others are defined directly in their respective core classes (e.g. `CV32E40P`).

To define a RISC-V core in your simulation, you must edit the Renode Platform file (.repl) and add a node for the CPU.

## Picking specific ISA variants

Start by adding `CPU.RiscV32` or `CPU.RiscV64` to the .repl file:
```
cpu: CPU.RiscV32 @ sysbus
```
then use the `cpuType` argument to specify the ISA and the required extensions.

Start with "rv32" or "rv64", depending on the architecture width, followed by a list of enabled ISA sets.
Extensions with names longer than one character have to be separated by an underscore.

For example:
```
cpu: CPU.RiscV32 @ sysbus
  cpuType: "rv32imaf_zicsr_zifencei"
```
which denotes a 32-bit RISC-V with the base instruction set (I), integer multiplication and division (M), atomic instructions (A), single-precision floating-point (F), CSR instructions (Zicsr), and instruction-fetch fence (Zifencei).

## Customizing the CPU

There are additional parameters you can pass to the CPU while creating it in the .repl file.
All of these are optional.

- `timeProvider` - sets the peripheral to be used as the time provider for the CPU, which is used to populate the `time` CSR. Typically you would provide your instance of the `clint` interrupt controller
- `privilegedArchitecture` - selects which version of the Privileged Architecture the CPU should follow. The default is 1.11. Available values are:
  - `PrivilegedArchitecture.Priv1_09`
  - `PrivilegedArchitecture.Priv1_10`
  - `PrivilegedArchitecture.Priv1_11`
  - `PrivilegedArchitecture.Priv1_12` - Currently support for Privileged Architecture v1.12 is experimental and not everything is implemented.
- `endianness` - specifies the endianness of the CPU, defaulting to little endian
- `nmiVectorAddress` and `nmiVectorLength` - allow for customizing the non-maskable interrupt vector, if supported by the CPU
- `allowUnalignedAccesses` - defines if an exception should be raised whenever the software performs an unaligned access on memory. Defaults to `false`
- `interruptMode` - Allows you to enforce interrupt handling mode. Defaults to auto. Available modes:
  - Auto (0) - Checks `mtvec`'s LSB to detect the mode
  - Direct (1) - All exceptions set `PC` to `mtvec`'s `BASE` value
  - Vectored (2) - Asynchronous interrupts set `PC` to `mtvec`'s `BASE + 4 * cause`
- `privilegeLevels` - specifies implemented privilege levels of the CPU. The default is Machine, Supervisor and User modes. Available values are:
  - `PrivilegeLevels.Machine`
  - `PrivilegeLevels.MachineUser`
  - `PrivilegeLevels.MachineSupervisorUser`

## Adding a custom RISC-V instruction

One of the most important features of RISC-V is its customizability, also with non-standard instructions.

There are several ways in which a custom instruction can be added to a RISC-V CPU in Renode.

They all revolve around two arguments
- Pattern - A bit pattern which specifies which instructions to match to execute your custom handler. Characters `1` and `0` denote which bit has to be set in that position, while any other character means "any value". The pattern has to have a length of 64, 32, or 16 characters.
- Handler - The code to execute when the pattern matches

### Python

You can use a {ref}`Python script <python-riscv>` for handling custom instructions by using the `InstallCustomInstructionHandlerFromString` or `InstallCustomInstructionHandlerFromFile` methods present on RISC-V CPUs.

For example:
```
sysbus.cpu InstallCustomInstructionHandlerFromString "10110011100011110000111110000010" "cpu.DebugLog('custom instruction executed!')"
```
The Python script has the `instruction` variable available, which contains the opcode of the instruction that was called.

### C#

You can use a C# function for handling custom instruction by using the `InstallCustomInstruction` method. It takes the same pattern argument, but the handler argument is `Action<UInt64>`

```csharp
public class MyCustomRiscV : RiscV32
{
    public MyCustomRiscV(IMachine machine, IRiscVTimeProvider timeProvider = null, uint hartId = 0,
                    PrivilegedArchitecture privilegedArchitecture = PrivilegedArchitecture.Priv1_11,
                    Endianess endianness = Endianess.LittleEndian, string cpuType = "rv32imfc_zicsr_zifencei")
      : base(machine, cpuType, timeProvider, hartId, privilegedArchitecture, endianness, allowUnalignedAccesses : true)
    {
      // As mentioned, the pattern arguments takes a 16, 32, or 64 character long string.
      // Characters 0 and 1 specify the bits that should be set,
      // while all other characters mean that given bit can be either 1 or 0.
      // In this case we use F for the Imm field, B for rs1, and D for rD to make the pattern more readable
      //
      // FFFFFFFFFFFFBBBBB100DDDDD0001011
      //      |        |       +-- [ 7:11] - rD
      //      |        +---------- [15:19] - rs1
      //      +------------------- [20:31] - Imm
      //
      // We could've used "-----------------100-----0001011" as the pattern and it'd mean the same thing,
      // but suddenly it's not so clear where the different fields are inside the opcode we're matching.
      InstallCustomInstruction(pattern: "FFFFFFFFFFFFBBBBB100DDDDD0001011", handler: opcode =>
      {
        this.Log(LogLevel.Noisy, "(p.lbu rD, Imm(rs1!)) at PC={0:X}", PC.RawValue);
        // rD = Zext(Mem8(rs1))
        var rD = (int)BitHelper.GetValue(opcode, 7, 5); // Extract value from opcode starting at bit 7 and length of 5
        var rs1 = (int)BitHelper.GetValue(opcode, 15, 5); // Extract value from opcode starting at bit 15 and length of 5
        var rs1Value = (long)GetRegisterUnsafe(rs1).RawValue;
        SetRegisterUnsafe(rD, ReadByteFromBus((ulong)rs1Value));

        // rs1 += Imm[11:0]
        var imm = (int)BitHelper.SignExtend((uint)BitHelper.GetValue(opcode, 20, 12), 12); // Extract value from opcode starting at bit 20 and length of 12
                                                                                           // and sign-extend it to full int
        SetRegisterUnsafe(rs1, (ulong)(rs1Value + imm));
      });
    }
}
```


### Verilated Custom Function Units

You can connect up to 4 CFUs to every RISC-V core that's simulated in Renode.

After you've compiled your CFU with the Verilator Integration Library (see: [Example CFU project](https://github.com/antmicro/renode-verilator-integration/blob/master/samples/cfu_mnv2/README.md)) you can attach the CFU to your CPU.

To do so, add this line to your .repl:
```
cfu0: Verilated.CFUVerilatedPeripheral @ cpu 0
```
and this line to your .resc:
```
cpu.cfu0 SimulationFilePathLinux @<PATH_TO_COMPILED_CFU_BINARY>
```

If you're on Windows as opposed to Linux you must use `SimulationFilePathWindows`, and respectively `SimulationFilePathMacOS` on macOS.
Instructions referencing your CFU will then be forwarded to the Verilated CFU.

All CFU instructions follow this pattern: `FFFFFFFAAAAABBBBBIIICCCCCNN01011`
- `N` - CFU number to forward the instruction call to
- `C` - Register in which the resulting value will be placed
- `I`, `F` - Function ID. The final ID that's passed to the CFU is `FFFFFFFIII`
- `B` - Source register 1. Its value will be read and passed into the CFU
- `A` - Source register 2. Same as the above

## Adding a custom RISC-V Control and Status Register

In a similar fashion to custom instructions, you can also define custom CSRs.

### Python

To use a {ref}`Python script <python-riscv>` to handle your custom CSR you can use `RegisterCSRHandlerFromString` and `RegisterCSRHandlerFromFile`.
The first argument is the CSR ID, while the second refers to the handler script.

The script gets passed a `request` variable, which contains fields `isRead`, `isWrite`, and `value`.

```python
if request.isRead: # If the CPU tries to read your CSR, isRead will be True
    cpu.DebugLog('CSR read!')
elif request.isWrite: # Otherwise isWrite will be True and value will contain the value being written
    cpu.DebugLog('CSR written: {}!'.format(hex(request.value)))
```

### C#

To use C# functions to handle custom CSRs you can use the `RegisterCSR` method.
Similarly it takes the ID as the first argument, but then takes the read handler and the write handler separately, in that order.

Let's take the previously defined custom RISC-V CPU and add a custom CSR to it which will return a random value every time it's read.

```csharp
public class MyCustomRiscV : RiscV32
{
    public MyCustomRiscV(IMachine machine, IRiscVTimeProvider timeProvider = null, uint hartId = 0,
                    PrivilegedArchitecture privilegedArchitecture = PrivilegedArchitecture.Priv1_11,
                    Endianess endianness = Endianess.LittleEndian, string cpuType = "rv32imfc_zicsr_zifencei")
      : base(machine, cpuType, timeProvider, hartId, privilegedArchitecture, endianness, allowUnalignedAccesses : true)
    {
      this.random = EmulationManager.Instance.CurrentEmulation.RandomGenerator;

      InstallCustomInstruction(pattern: "FFFFFFFFFFFFBBBBB100DDDDD0001011", handler: opcode =>
      {
        // Custom Instruction implementation from before
      });

      RegisterCSR(
        (ulong)CustomCSR.Rnd,
        () => (ulong)random.Next(),           // Read handler
        value => { /* Ignore all writes */ }, // Write handler
        name: "RND"                           // Optionally add a name of your CSR
      );
    }

    private readonly PseudorandomNumberGenerator random;

    // Creating an enum isn't required, but it's cleaner
    // and allows to name otherwise arbitrary CSR IDs
    private enum CustomCSR : ulong
    {
      Rnd = 0xfc0,
    }
}
```
