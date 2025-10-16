# Monitor and script syntax

The Monitor is Renode's command line interface (CLI).
It lets you talk to Renode and control the emulation using a wide range of built-in functions.
They allow you to access emulation objects like peripherals, machines, and external connectors.

```{note}
If you want to learn more about the Monitor and its basic usage, visit the {doc}`../introduction/using` chapter.
```

Generally, commands in Renode are executed line-by-line, and the arguments need to be separated by a space character.
You can further extend the range of available functions with Python (see [monitor.py](https://github.com/renode/renode/blob/master/scripts/monitor.py) for examples and {doc}`using-python` for instructions how to use Python to extend Renode).

## Using built-in commands

Renode comes with dozens of built-in commands.
You can access the full list of commands with their descriptions using the `help` command in the Monitor.
To get more detailed information about a certain command, use `help <command>`, e.g.:

```
help start
```

## Accessing emulation objects

To get access to commands available to your machine's emulation objects (e.g., peripherals), you can type the object's name and click Tab twice to activate tab completion.

Emulation objects are in a hierarchy, with `sysbus` being a machine's root for all peripherals.
If you want to access a UART peripheral of your machine called `uart`, you need to use `sysbus.uart`.
You can use `using` command to set a default prefix, e.g. `using sysbus` allows you to refer to the UART directly:

```
uart
```

You will find that the `using sysbus` command is used in most of the scripts bundled with Renode.

Passing the name of the emulation object as a command returns the full list of available methods, properties, and value fields for this object.
In this list, you can find information on whether the method returns a value, what data types it accepts, and how to use it:

```none
(machine-0) uart
The following methods are available:
 - Void AddLineHook (String contains, String pythonScript)
 - Void CloseFileBackend (String path)
 - Void CreateFileBackend (String path, Boolean immediateFlush = False)
 - Void DebugLog (String message)
 - String DumpHistoryBuffer (Int32 limit = 0)
 - Endianess GetEndianness (Endianess? defaultEndianness = null)
 - IEnumerable<tuple<string,< span="">IGPIO>> GetGPIOs ()</tuple<string,<>
...
Usage:
 sysbus.uart MethodName param1 param2 ...
The following properties are available:
 - UInt32 BaudRate
     available for 'get'
 - Parity ParityBit
     available for 'get'
 - Int64 Size
     available for 'get'
 - Bits StopBits
     available for 'get'
Usage:
 - get: sysbus.uart PropertyName
 - set: sysbus.uart PropertyName Value
```

To inspect the parameters of a specific method available to an object, simply provide the name of the object and the method:

```none
(machine-0) uart WriteWordUsingByte
The following methods are available:
 - Void WriteWordUsingByte (Int64 address, UInt16 value)
Usage:
 sysbus.uart MethodName param1 param2 ...
```

Keep in mind that if a method does not require any parameters, providing its name will invoke it:

```none
(machine-0) machine GetTimeSourceInfo
Elapsed Virtual Time: 00:00:00.000000
Elapsed Host Time: 00:00:00.000000
Current load: NaN
...
```

Many commands require you to specify a parameter after the command when using them:

```none
using sysbus
```

## Accessing attributes of an object

Objects in Renode have access to different methods, properties, fields, and indexers depending on their type.
The methods are required to access the parameters of a peripheral, and to do it successfully, you need to follow this syntax:

```none
(machine) registrationPoint.peripheral MethodName param1 param2
```

To read the value of a byte at offset 0 from the `uart` peripheral registered on the `sysbus` you would type:

```none
(machine-0) sysbus.uart ReadByte 0
```

Renode enables you to both get and set values for the object's attributes.
If you do not specify a value at the end of your command, the current value will be returned.
If you want to set a value, you need to use the proper command and value at the end.

For example, to set the `CyclesPerInstruction` property to `0x000002`, you would use:

```none
(machine-0) cpu CyclesPerInstruction 0x000002
```

To get the value of this newly set property, you have to use:

```none
(Mi-V) cpu CyclesPerInstruction
0x00000002
```

Setting indexers is very similar to setting properties, with the main difference being that you have to put your parameters in the square brackets:

```none
(machine-0) machine IndexerName [param1 param2 ...] Value
```

To get the value of the indexer, use:

```none
(machine-0) machine IndexerName [param1 param2 ...]
```

The last type of emulation object attribute is a field.
Their values can be accessed the same as you access properties:

```none
(machine-0) machine SystemBusName
sysbus
```

## Command substitution with backticks

The Monitor allows you to use the output of one command as an argument to another.
This can be achieved by enclosing a command in backticks (`` ` ``), similarly to how it’s done in Unix-like shells.

The command inside the backticks is executed first, and its output is then used as an argument in the outer command.
For example, you can find the symbol at the current program counter (`PC`) of the CPU by running:

```none
(machine-0) sysbus FindSymbolAt `cpu PC`
```

In this case, `cpu PC` is executed first, and its output (the current value of the program counter) is then passed to the `sysbus FindSymbolAt` command.

## Operating on enumerable properties

Some peripherals and properties are enumerable, which means they can contain multiple elements.
A good example of this is a CPU cluster, which consists of several cores.
You can operate on all elements of such a collection at once using the `ForEach` and `Select` commands.

The `ForEach` command allows you to execute an action on each element of a collection.
For example, to halt all cores in `cluster0`, you can run:

```none
(machine-0) cluster0 ForEach IsHalted true
```

The `Select` command, on the other hand, allows you to transform each element of a collection.
For example, to get the value of the X0 register on each core in a cluster:

```none
(machine-0) cluster0 Select GetRegister "X0"
[
0xaaaac4db0770, 0xffff795b42148000, 0x5, 0x5,
]
```

Or, to get the `SFDPSignature` of a flash memory as a list of decimal strings, you can use:

```none
(machine-0) qspi.spiFlash SFDPSignature Select ToString "d"
[
83, 70, 68, 80, 6, 1, 0, 255, 255, 255,
255, 255, 255, 255, 255, 255,
]
```

## Supported data types

The Monitor supports a wide variety of data types:

```{list-table} Data types supported by the Monitor
:header-rows: 1
:widths: 50 50
* - Name of the data type
  - Example
* - comment
  - #comment or :comment
* - integer
  - 1
* - float
  - 1.1
* - hexadecimal
  - 0xfffff000
* - strings
  - "string"
* - range
  - <0xdefg, 0xefgh>
* - relative range
  - <0x6 0x2>
* - index
  - [0]
* - path
  - @path/to/file or @path\ with\ spaces
* - logical values
  - true or false (case insensitive)
* - variables and macros
  - $var
* - enum
  - Literal
```

```{note}
You can pass the `path` parameter to a function that accepts `strings` and it will be converted to a `string`.
Keep in mind that the additional filename autocompletion is only available after an `@` sign.
```

## Monitor variable types

There are three ways you can create a single line variable in the Monitor:

* `$var="hello"`,
* `$var?="hello"`,
* `set var "hello"`.

The difference between `$var=` and `$var?=` is that the latter indicates a default value if the variable is not set.
The Monitor also enables you to create multiline variables using the following syntax:

```none
set var """
"hello"
"""
```

````{note}
When loading a script, you can use slightly different syntax for multiline variables, with the `"""` mark put below the first line:

```none
set var
"""
"hello"
"""
```
````

Variables in Renode are contextual, which means that for each machine you can have different variables with the same name.
You can access them by their full path.
To create a variable within the machine context of `machine-0`, you would use:

```none
(machine-0) $machine_0.var
```

You can also create global variables if you use the `global` prefix:

```none
(monitor) $global.CWD
```

Most of the time, a short name (without the context prefix) should be enough to access variables.

The Monitor gives you access to two special variables: `$ORIGIN` and `$CWD`.

Other types of variables available in Renode are macros, which enable you to encapsulate fragments of your script and execute them easily.
You can set a new macro using the `macro` command with the name of the new variable and the commands you want it to execute:

```none
macro newMacro
> sysbus LoadELF $bin
```

You can create multiline macros using the Monitor multiline syntax.
You can then execute your newly created macro using the `runMacro` command:

```none
runMacro $newMacro
```

You can notice that many Renode sample scripts define the `$reset` macro.
This macro is used whenever the `machine Reset` method is called by the user or via the simulation logic.

## File paths

Each Renode project will require you to supply the file path to the components necessary for your project.
The vast majority of them use the `@` sign, which activates autocompletion suggestions and represents a path to a file:

```none
include @/path/to/platform.repl
```

When interpreting a path, Renode looks in several places based on the configured internal `path`.
By default:

* it first checks in the Renode root directory,
* if the file was not found in the root directory, it checks the current working directory.

You can check and modify the path configuration using the `path` command in Monitor.

You can also pass paths as `"string"`, but completion suggestions will not work in that case.

```{note}
In Renode, you can use paths that are absolute or relative to the current directory.
```

### Relative paths

If you want to express a path that is relative to the currently executed Renode script (.resc) you can use the `$ORIGIN` variable:

```none
include $ORIGIN/my_subscript.resc
```

An example of usage can be found in [the fomu script](https://github.com/renode/renode/blob/8ae7fdfc6cbe7b01952a8b2d4517d14aff7a297e/scripts/complex/fomu/renode_etherbone_fomu.resc#L5).

```{note}
Do not use `@` at the beginning of an `$ORIGIN`-based path.
```

Keep in mind that the `$ORIGIN` variable is only available inside a script - it won't work interactively in Monitor.

In Monitor, you can use a special `$CWD` variable to provide a path that is relative to the current working directory:

```none
(machine-0) include $CWD/my_script.resc
```

```{note}
There is no `@` at the beginning of the `$CWD`-based path.
```

```{note}
In a Robot file, you can also use another variable: `${CURDIR}`.
It is handled and resolved on the Robot Framework level and has nothing to do with Renode.
Paths starting with `${CURDIR}` are relative to the Robot file location.

An example of usage can be found in [the LSM9DS1 test](https://github.com/renode/renode/blob/8ae7fdfc6cbe7b01952a8b2d4517d14aff7a297e/tests/peripherals/LSM9DS1.robot#L24).

A ``${CURDIR}``-based paths need to be prepended with ``@``.
Since it is resolved at the Robot Framework level, for Renode, it looks like any other path provided by a user.

If you want to learn more about testing with Renode, visit [chapter devoted to this topic](../introduction/testing.md).
```

(renode-script-syntax)=
## Renode Script syntax

Many of your projects in Renode will involve using the same platforms and commands multiple times.
This process can be accelerated significantly using `.resc` files, which are Renode scripts.
The syntax of `.resc` files is the same as that of the Monitor.

To load a Renode script, use the `include` or `i` command:

```none
include @/path/to/script.resc
```

```{note}
You can use the `start` command instead of `include` to start your emulation immediately.
```

The syntax of a `.resc` file can be exemplified using one of many scripts built into Renode, like [Nordic Semiconductor NRF52840 script](https://github.com/renode/renode/blob/master/scripts/single-node/nrf52840.resc), which we will cover line by line:

```none
:name: nRF52840
:description: This script runs Zephyr Shell demo on NRF52840.

using sysbus

mach create
machine LoadPlatformDescription @platforms/cpus/nrf52840.repl

$bin?=@https://dl.antmicro.com/projects/renode/renode-nrf52840-zephyr_shell_module.elf-gf8d05cf-s_1310072-c00fbffd6b65c6238877c4fe52e8228c2a38bf1f

showAnalyzer uart0

macro reset
"""
    sysbus LoadELF $bin
"""
runMacro $reset
```

The first two lines are comments, and they are not interpreted by the Monitor:

```none
:name: nRF52840
:description: This script runs Zephyr Shell demo on NRF52840.
```

Next, we utilize the `using` command to omit a prefix when referring to a peripheral.
The command `using sysbus` enables you to refer to the CPU device with `cpu` instead of `sysbus.cpu`:

```none
using sysbus
```

Then, we create a new machine

```none
mach create
```

We load a platform description from the `.repl` file:

```none
machine LoadPlatformDescription @platforms/cpus/nrf52840.repl
```

Now, we load a sample shell binary:

```none
$bin?=@https://dl.antmicro.com/projects/renode/renode-nrf52840-zephyr_shell_module.elf-gf8d05cf-s_1310072-c00fbffd6b65c6238877c4fe52e8228c2a38bf1f
```

Next, we set up an UART analyzer for `uart0`:

```none
showAnalyzer uart0
```

The next element of our script is a macro, which is executed every time the machine is reset.

To create a macro in your `.resc` you need to surround your macro's code with `"""` (3 double quotation marks).
The contents of your macro do not need to be indented with four spaces, but we often do it for readability.

The macro below loads the previously specified ELF file:

```none
    sysbus LoadELF $bin
```

Lastly, we call the macro to run it, as it is only executed after it is invoked:

```none
runMacro $reset
```
