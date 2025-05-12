# Peripheral modeling guide

Renode allows the user to "model" HW peripherals in several ways:

* {rsrc}`automatic tags from the SVD file </platforms/cpus/nrf52840.repl#L115>` used mainly for logging purposes,
* {rsrc}`manual tags with return value </platforms/cpus/vybrid.repl#L106>` used for logging and trivial flow control,
* {rsrc}`Python peripherals </platforms/cpus/tegra3.repl#L134-L137>` used for implementing very simple logic,
* C# models, used to describe advanced peripheral logic and interconnect - described in details below.

## How does access to the system bus work?

`read`/`write` operations executed by the CPU (usually in the C implementation in the `tlib` submodule) are either directed to the internal memory or passed to the system bus and handled by the framework at the C# level.

Access to the memory modeled as {risrc}`MappedMemory </src/Emulator/Main/Peripherals/Memory/MappedMemory.cs>` is handled entirely at the C level, all other operations are passed from C to C# via
{risrc}`TranslationCPU.Read{Byte,Word,DoubleWord,QuadWord}FromBus </src/Emulator/Peripherals/Peripherals/CPU/TranslationCPU.cs#L609-L674>`/
{risrc}`TranslationCPU.Write{Byte,Word,DoubleWord,QuadWord}ToBus </src/Emulator/Peripherals/Peripherals/CPU/TranslationCPU.cs#L677-L746>` functions.

NOTE: It is possible to change {risrc}`MappedMemory </src/Emulator/Main/Peripherals/Memory/MappedMemory.cs>` type to
{risrc}`ArrayMemory </src/Emulator/Main/Peripherals/Memory/ArrayMemory.cs>` in order to handle all memory operations at the C# level.
Keep in mind this might cause a significant drop in performance.


    ┌──────────────┐  C to C   ┌─────────────┐
    │ MappedMemory │ ◀──────── │     CPU     │
    └──────────────┘           └─────────────┘
                                 │
                                 │ C to C#
                                 ▼
    ┌──────────────┐           ┌─────────────┐     ┌─────────────┐
    │ Peripheral1  │ ◀──────── │  SystemBus  │ ──▶ │ Peripheral2 │
    └──────────────┘           └─────────────┘     └─────────────┘
                                 │
                                 │
                                 ▼
                               ┌─────────────┐
                               │ ArrayMemory │
                               └─────────────┘

## What if there is no peripheral mapped at given offset?

In the case of write, the operation will be ignored and a warning message will be generated in the log.

In the case of read, the default value of 0 will be returned and a warning message will be generated in the log.

## What happens when the peripheral does not implement the given access width?

By default this situation is treated as if there was no peripheral mapped at a given offset.

It is, however, possible to enable automatic translation of access type at the peripheral level using the {risrc}`AllowedTranslation </src/Emulator/Main/Peripherals/Bus/AllowedTranslationsAttribute.cs>` attribute - see an {risrc}`example of usage </src/Emulator/Peripherals/Peripherals/Timers/LiteX_Timer.cs#L18>`.

Note that automatic translation might generate more accesses on the bus, e.g., 4 byte reads per one double word read or 1 double word read and one double word write per one byte write.
This might have unintended side effects for some registers, e.g., automatically incrementing FIFO data register, issuing the "read-to-clear" behavior or others, depending on the registers' semantics.
It is up the developer to verify if the automatic translation is safe in the context of a given peripheral model.

## Writing a peripheral model in C#

A C# class is considered a peripheral model if it implements the {risrc}`IPeripheral </src/Emulator/Main/Peripherals/IPeripheral.cs>` interface.

In order for the peripheral to be attachable to the system bus, it must implement at least one (but can implement a few) of:
{risrc}`IBytePeripheral </src/Emulator/Main/Peripherals/Bus/IBytePeripheral.cs>`,
{risrc}`IWordPeripheral </src/Emulator/Main/Peripherals/Bus/IWordPeripheral.cs>`,
{risrc}`IDoubleWordPeripheral </src/Emulator/Main/Peripherals/Bus/IDoubleWordPeripheral.cs>`,
{risrc}`IQuadWordPeripheral </src/Emulator/Main/Peripherals/Bus/IQuadWordPeripheral.cs>` interfaces, enabling 8, 16, 32 and 64-bit accesses respectively.

Double word bus peripherals must implement at least three methods:

* for reading (e.g., {risrc}`ReadDoubleWord </src/Emulator/Main/Peripherals/Bus/IDoubleWordPeripheral.cs#L13>`) - called by the system bus in order to read a value from the peripheral,
* for writing (e.g., {risrc}`WriteDoubleWord </src/Emulator/Main/Peripherals/Bus/IDoubleWordPeripheral.cs#L14>`) - called by the system bus in order to write a value to the peripheral,
* for resetting ({risrc}`Reset </src/Emulator/Main/Peripherals/IPeripheral.cs#L23>`) - called by the framework to restore the state of the peripheral to the initial state.

Although it's technically possible to implement `read`/`write` method in any way, the preferred one is to use the Register Framework ({risrc}`the source code </src/Emulator/Main/Core/Structure/Registers>`).
For an example of usage, see {risrc}`the LiteX UART </src/Emulator/Peripherals/Peripherals/UART/LiteX_UART.cs#L20-L52>`.

You can even use a base class (`Basic{Byte,Word,DoubleWord}Peripheral`) to simplify the code - see an {risrc}`example </src/Emulator/Peripherals/Peripherals/Timers/LiteX_CPUTimer.cs>`.

The following section explains how to design a peripheral using the Register Framework.

## Register modeling guidelines

Create a private enum, preferably named `Registers`, that lists **all** registers supported by the peripheral.
Conforming to the enum naming convention (or marking it with the {risrc}`RegistersDescription </src/Emulator/Main/Peripherals/Bus/Wrappers/RegisterMapper.cs#L72>` interface) allows the system bus to generate better log messages by including register name in logs generated by `sysbus LogPeripheralAccess`.

Use human-readable, PascalCase encoded names (i.e., `InterruptEnable` instead of `IEN`) even if they are referred to differently in the documentation.
As values of the enum fields, use the offset from the beginning of the peripheral's memory space (i.e., offsets relative to the beginning of the peripheral, **not** absolute addresses).
Keep in mind that a platform can have multiple peripherals of a given type.
Please be reasonable here - there are sometimes peripherals with too many registers or registers forming {risrc}`a repeatable pattern </src/Emulator/Cores/RiscV/PlatformLevelInterruptController.cs#L77-L103>` - in such case a creative approach is encouraged.

Do not **implement** all registers - only those that are actually used by the software and can be therefore tested.

For each register **list** all fields but **implement** only the necessary ones.
Fields that are not implemented should be marked as tags, reserved or ignored - this will help generating better access logs.

There are different type of fields available in Registers Framework:

* flags - single-bit fields ({risrc}`example </src/Emulator/Peripherals/Peripherals/Timers/LiteX_Timer.cs#L125>`),
* enum fields - single-or-multiple bit fields where bit patterns encode some non-numeric value ({risrc}`example </src/Emulator/Peripherals/Peripherals/SD/LiteSDCard.cs#L138>`),
* value fields - single-or-multiple bit fields encoding a numeric value ({risrc}`example </src/Emulator/Peripherals/Peripherals/SD/LiteSDCard.cs#L133>`).

For each field you can select an access mode (Read&Write by default) that defines which operations are allowed and how they are handled by the framework.
Possible basic values (that can be combined together with a bitwise `| OR` operator) are:

* `Read`,
* `Write`,
* `Set` - writing `1` sets the bit, writing `0` has no effect,
* `Toggle` - writing `1` toggles the current value, writing `0` has no effect [this is most likely usable for flag fields only],
* `WriteOneToClear` - writing `1` clears the bit, writing `0` has no effect [this is most likely usable for fields flag only],
* `WriteZeroToClear` - writing `0` clears the bit, writing `1` has no effect [this is most likely usable for fields flag only],
* `ReadToClear` - the value is set to 0 after read.

Writing a non-zero value to a read-only field will be ignored and generate a warning in the log.
Reading from the write-only field will return the default value of 0 (but will not generate a warning in the log, as it's impossible to infer which fields are read).

By default each register provides an automatic backing field. It means that the software will read the previously written value (assuming that fields are writable and readable).
It is possible to access the backing field and modify its value from the code. In order to do that use an `out` parameter - see {risrc}`an example </src/Emulator/Peripherals/Peripherals/UART/LiteX_UART.cs#L42>`.

There are helper methods for generating groups of registers - see the {risrc}`DefineMany </src/Emulator/Peripherals/Peripherals/Timers/LiteX_Timer.cs#L60-L68>` usage example.

It is also possible to attach callbacks for situations when the field is:

* written (with any value) ({risrc}`example </src/Emulator/Peripherals/Peripherals/UART/LiteX_UART.cs#L23>`),
* changed (written with a value different than the current one) ({risrc}`example </src/Emulator/Cores/X86/LAPIC.cs#L172>`),
* read (the value is taken from the backing field) ({risrc}`example </src/Emulator/Peripherals/Peripherals/Network/LiteX_Ethernet_CSR32.cs#L321>`),
* read - value provider (the value is generated by the callback itself) ({risrc}`example </src/Emulator/Peripherals/Peripherals/UART/LiteX_UART.cs#L24>`). 

There are also callbacks for the whole register - {risrc}`WriteCallback </src/Emulator/Peripherals/Peripherals/I2C/OpenCoresI2C.cs#L64>` and {risrc}`ReadCallback </src/Emulator/Peripherals/Peripherals/Timers/EFR32_RTCC.cs#L173>`. They are useful when the value of multiple fields is necessary for the callback logic.

## Bus peripheral size

In most cases the size of the peripheral on the bus is well defined and can be included in the model.
In order to do that, the class must implement the {risrc}`IKnownSize </src/Emulator/Main/Peripherals/IKnownSize.cs>` interface.
The size encoded in the `Size` property is expressed in bytes.

Note: Peripherals **not** implementing the `IKnownSize` interface can be also used in Renode, but it is required to provide the size each time {rsrc}`the device is registered </platforms/cpus/stm32f746.repl#L26>` (in the repl file).

## Testing guidelines

For a peripheral to be pushed to Renode upstream repository, it is required that a test is provided, executing at least one binary.
The preferred way of testing peripherals is to use standard tests/samples if available, e.g. Zephyr samples, driver tests etc. or provide a custom specific binary.
All testing binaries should be buildable from sources.

The test case should be described in Robot Framework.
See {rsrc}`examples </tests/platforms>` of simple tests.

## Example peripherals

Here is a list of various Renode peripheral models that can be used as an inspiration:

* {risrc}`UART </src/Emulator/Peripherals/Peripherals/UART/LiteX_UART.cs>`
* {risrc}`Timer </src/Emulator/Peripherals/Peripherals/Timers/LiteX_Timer.cs>`
* {risrc}`GPIO controller </src/Emulator/Peripherals/Peripherals/GPIOPort/MPFS_GPIO.cs>`
* {risrc}`I2C controller </src/Emulator/Peripherals/Peripherals/I2C/MPFS_I2C.cs>`
* {risrc}`SPI controller </src/Emulator/Peripherals/Peripherals/SPI/MPFS_SPI.cs>`
* {risrc}`I2C sensor </src/Emulator/Peripherals/Peripherals/Sensors/SI70xx.cs>`
* {risrc}`SPI sensor </src/Emulator/Peripherals/Peripherals/Sensors/TI_LM74.cs>`

## Automatic generation of peripheral stubs

To avoid writing the register layout by hand, Renode provides a tool to automate the process - to "scaffold" a generic peripheral structure, thus enabling the developer to focus mostly on implementing the behavioral logic.
The [peakrdl-renode](https://github.com/renode/renode/tree/master/tools/PeakRDL-renode) tool works by parsing a peripheral's memory map described in the [SystemRDL](https://www.accellera.org/downloads/standards/systemrdl) file, and outputting an autogenerated file containing a `partial` class.

The class has to be then supplemented by writing custom logic, describing the behavior of the peripheral.
This allows the developers to simplify the manual and error-prone process of codifying the registers, which can be especially useful during the hardware development phase, where the devices' register layout is not yet stable.
SystemRDL data can also be used as a source of truth for software and RTL development, ensuring a consistent state of various parts of the project.

Renode provides an example of an autogenerated peripheral in the repository:
* {risrc}` Caliptra I3C autogenerated part <src/Emulator/Peripherals/Peripherals/I3C/Caliptra_I3C_generated.cs>`
* {risrc}` Caliptra I3C behavioral logic <src/Emulator/Peripherals/Peripherals/I3C/Caliptra_I3C.cs>`

Only the logic is written by hand, the autogenerated file shouldn't be modified at all.

This sample demonstrates that for large models containing dozens or hundreds of registers, the tool substantially improves the development process.

To start using the `peakrdl-renode` tool, execute the following commands:
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install peakrdl
pip install git+https://github.com/renode/renode/#subdirectory=tools/PeakRDL-renode
```
Run `peakrdl renode --help` to verify that the tool was installed correctly.

You can experiment with a very basic model to see how the tool behaves.

Let's create a sample SystemRDL file, describing a layout of a peripheral.
```systemrdl
addrmap Peripheral {
    regfile {
        default regwidth = 32;

        reg {
            name = "BitFields";
            field {
                name = "FIRST";
                sw = r;
                hw = w;
            } first [0:0];
            field {
                name = "SECOND";
                sw = rw;
                hw = rw;
                onwrite = wzc;
            } second [1:5];
        } bit_fields @ 0x0;

        reg {
            field {
                name = "FIRST";
                sw = rw;
                hw = rw;
            } first [0:0];
        } also_bit_fields @ 0x10;
    } registers @ 0x100;
};
```
To generate the C# scaffolding, assuming that the source file is named `peripheral.rdl`, run:
```sh
peakrdl renode -n MyPeripheral -N Miscellaneous -o MyPeripheral_generated.cs peripheral.rdl
```

The result should look similar to this:
```csharp
// Generated by PeakRDL-renode

using Antmicro.Renode.Core.Structure.Registers;
using Antmicro.Renode.Peripherals.Bus;

namespace Antmicro.Renode.Peripherals.Miscellaneous
{
    public partial class MyPeripheral : IProvidesRegisterCollection<DoubleWordRegisterCollection>, IPeripheral, IDoubleWordPeripheral
    {
        /// <summary> Register "registers.bit_fields" at 0x100 </summary>
        protected Registers_BitFieldsType Registers_BitFields;
        /// <summary> Register "registers.also_bit_fields" at 0x110 </summary>
        protected Registers_AlsoBitFieldsType Registers_AlsoBitFields;

        public DoubleWordRegisterCollection RegistersCollection { get; }

        public MyPeripheral()
        {
            RegistersCollection = new DoubleWordRegisterCollection(this);
            Registers_BitFields = new Registers_BitFieldsType(this);
            Registers_AlsoBitFields = new Registers_AlsoBitFieldsType(this);
            this.Init();
        }

        partial void Init();

        partial void Reset();

        void IPeripheral.Reset()
        {
            this.Reset();
            RegistersCollection.Reset();
        }

        uint IDoubleWordPeripheral.ReadDoubleWord(long offset)
        {
            return RegistersCollection.Read(offset);
        }

        void IDoubleWordPeripheral.WriteDoubleWord(long offset, uint value)
        {
            RegistersCollection.Write(offset, value);
        }

        public struct Registers_BitFieldsType
        {
            /// <summary> Field "first" at 0x0, width: 1 bits </summary>
            public IFlagRegisterField FIRST;
            /// <summary> Field "second" at 0x1, width: 5 bits </summary>
            public IValueRegisterField SECOND;

            public Registers_BitFieldsType(IProvidesRegisterCollection<DoubleWordRegisterCollection> parent)
            {
                parent.RegistersCollection.DefineRegister(0x100, 0x0, true)
                    .WithFlag(0, out FIRST, mode: FieldMode.Read, name: "FIRST")
                    .WithValueField(1, 5, out SECOND, mode: FieldMode.Read | FieldMode.WriteZeroToClear, name: "SECOND");
            }
        }

        public struct Registers_AlsoBitFieldsType
        {
            /// <summary> Field "first" at 0x0, width: 1 bits </summary>
            public IFlagRegisterField FIRST;

            public Registers_AlsoBitFieldsType(IProvidesRegisterCollection<DoubleWordRegisterCollection> parent)
            {
                parent.RegistersCollection.DefineRegister(0x110, 0x0, true)
                    .WithFlag(0, out FIRST, name: "FIRST");
            }
        }
    }
}
```

Having this file generated, you can create a second file, `MyPeripheral.cs`, and start by implementing the `Init` and `Reset` methods.
Then, you can refer to the individual registers' fields, e.g. by attaching callbacks, as shown in the snippet below, in the `AttachCallbacks` method.
```csharp
using Antmicro.Renode.Core.Structure.Registers;
using Antmicro.Renode.Peripherals.Bus;
using Antmicro.Renode.Logging;

public partial class MyPeripheral
{
    partial void Init()
    {
        // Add you logic here

        // This is an example of custom logic, achieved by attaching callbacks to registers
        AttachCallbacks();
        this.Reset();
    }

    partial void Reset()
    {
        // Add your logic here

        secondVal = 0;
    }

    private void AttachCallbacks()
    {
        // Example of callbacks attached to a register, implementing behavioral logic
        this.Registers_BitFields.FIRST.ValueProviderCallback += (val) =>
        {
            this.Log(LogLevel.Debug, "Previous FIRST value: {0}", val);
            // Test low bit of "secondVal"
            return (secondVal & 1) == 1;
        };
        this.Registers_BitFields.SECOND.WriteCallback += (old_val, new_val) =>
        {
            secondVal = new_val + 1;
            this.Log(LogLevel.Debug, "second_val: {0} -> {1}", old_val, secondVal);
        };
    }

    private ulong secondVal;
}

```


```{note}
For more information, refer to the [`peakrdl-renode`'s README](https://github.com/renode/renode/blob/master/tools/PeakRDL-renode/README.md)
```
