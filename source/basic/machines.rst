Working with machines
.....................

Renode allows to easily handle emulations spanning multiple machines.

Creating machines
'''''''''''''''''

At the beginning the emulation is empty - there is no machine to run.
In order to add an empty one, execute::

    (monitor) mach create
    (machine-0)

This creates the first machine, which - if you don't give it a custom name - will be indexed from 0 (and thus called machine-0).
This command also switches the Monitor's context to this new machine.

Executing the same command again will create another machine, called ``machine-1``::

    (machine-0) mach create
    (machine-1)

You can create a machine with a custom name by providing it as the argument::

    (monitor) mach create "my-machine"
    (my-machine)

To list all created machines together with their names and indices, type::

    (my-machine) help mach

Switching between machines
''''''''''''''''''''''''''

When you want to switch the Monitor's context to another machine type::

    (machine-1) mach set "machine-0"
    (machine-0)

Instead of the machine's name you can use its index as well::

    (machine-1) mach set 0
    (machine-0)

Loading platforms
'''''''''''''''''

Once a machine is created it contains only one peripheral - the *system bus* called simply ``sysbus``.
There is no memory or cpu, so it is not yet ready to execute any code.

To list all peripherals, execute::

    (machine-0) peripherals
    Available peripherals:
    sysbus (SystemBus)

To load a predefined platform (in this example *Microsemi MiV*), type::

    (machine-0) machine LoadPlatformDescription @platforms/cpus/miv.repl
    (machine-0) peripherals
    Available peripherals:
    sysbus (SystemBus)
    │
    ├── clint (CoreLevelInterruptor)
    │     <0x44000000, 0x4400FFFF>
    │
    ├── cpu (RiscV)
    │     Slot: 0
    │
    ├── ddr (MappedMemory)
    │     <0x80000000, 0x83FFFFFF>
    │
    ├── flash (MappedMemory)
    │     <0x60000000, 0x6003FFFF>
    │
    ├── gpioInputs (MiV_CoreGPIO)
    │     <0x70002000, 0x700020A3>
    │
    ├── gpioOutputs (MiV_CoreGPIO)
    │     <0x70005000, 0x700050A3>
    │
    ├── plic (PlatformLevelInterruptController)
    │     <0x40000000, 0x43FFFFFF>
    │
    ├── timer0 (MiV_CoreTimer)
    │     <0x70003000, 0x7000301B>
    │
    ├── timer1 (MiV_CoreTimer)
    │     <0x70004000, 0x7000401B>
    │
    └── uart (MiV_CoreUART)
          <0x70001000, 0x70001017>

Accessing and manipulating peripherals
''''''''''''''''''''''''''''''''''''''

When you are in the context of a machine in the Monitor you can reference peripherals by name.
You can read and write a peripheral's properties as well as execute some actions on them.
The set of available properties and operations depends on the type of peripheral.

For example to check memory size, execute::

    (machine-0) sysbus.ram Size

To call an action on the peripheral use the same syntax - replace ``Size`` with action name, e.g., ``ZeroAll``::

    (machine-0) sysbus.ram ZeroAll

To get the complete list of available properties or actions just enter the peripheral's name::

    (machine-0) sysbus.ram
    The following methods are available:
    - Void DebugLog (String message)
    - Void Dispose ()
    [...]
    - Void WriteWordUsingDwordBigEndian (Int64 address, UInt16 value)
    - Void ZeroAll ()
    Usage:
    sysbus.ram MethodName param1 param2 ...
    The following properties are available:
    - Int32 SegmentCount
        available for 'get'
    - Int32 SegmentSize
        available for 'get'
    - Int64 Size
        available for 'get'
    Usage:
    - get: sysbus.ram PropertyName
    - set: sysbus.ram PropertyName Value

The ``Usage`` sections describe the proper syntax for accessing the peripheral's features.

Loading binaries
''''''''''''''''

Once the platform is created and configured you can upload the software on it.
Renode allows you to run exactly the same executable as on the real hardware - there is no need to alter the binary or recompile the source.

To load an ELF file to memory, execute::

    (machine-0) sysbus LoadELF @my-project.elf

Renode supports other executable formats like raw *binary* and *UImage* as well.
To load them use ``LoadBinary`` or ``LoadUImage`` accordingly.

Clearing the emulation
''''''''''''''''''''''

If you want to switch to another project you can drop the whole emulation::

    (machine-0) Clear

All machines, peripherals and loaded binaries will be removed and Renode will return to its initial state.
