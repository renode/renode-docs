# Describing platforms

Renode uses a text-based format to describe platforms.
Platform description files typically have the `.repl` extension, but this is not a requirement.

The broad description of the format and its grammar is available in the [platform-description-format](../advanced/platform_description_format.md) section.
Here we present the basic usage and most common scenarios.

## Defining peripherals

To add a peripheral, you need to know its type, choose its name and the registration point.
Most peripherals will be registered on the `sysbus` - a peripheral that is always available and does not have to be explicitly defined.

The type name has to indicate the class of the peripheral model.
This has to be a full name with a namespace, but the default namespace, `Antmicro.Renode.Peripherals`, can be omitted.

For example, to create a UART object of type `Antmicro.Renode.Peripherals.UART.MiV_CoreUART`, connected to the system bus at `0x80000000`, use:

```none
uart0: UART.MiV_CoreUART @ sysbus 0x80000000
```

Some peripherals, like the mentioned UART, need parameters to be constructed.
The REPL format allows you to set the constructor parameters and properties of the peripheral model.
They are placed below the declaration, with four spaces of indentation:

```none
uart0: UART.MiV_CoreUART @ sysbus 0x80000000
    clockFrequency: 66000000
```

Constructor parameters begin with a lower case letter, and properties with an upper case letter.

## Connecting peripherals

In the example above the `uart0` peripheral was connected to the system bus at a specific address.
It is possible, however, to connect peripherals to other buses as well, like I2C or SPI, to a GPIO controller, etc.

For example, to connect a temperature sensor to an I2C controller called `i2c0` at `0x80`, type:

```none
sensor: Sensors.SI70xx @ i2c0 0x80
```

Peripherals can also be connected via GPIOs or interrupts.
Renode treats these signals similarly, and allows you to create a connection with the `->` operator.

To connect a timer to the 31-st interrupt on the `plic` interrupt controller, run:

```none
timer: Timers.MiV_CoreTimer @ sysbus 0x1000000
    -> plic @ 31
```

## Including files

You can include an existing REPL file in your platform with the `using` keyword.

The path will be looked up in each of the directories on the Monitor's internal `PATH`, which is editable with the `path` command.
By default, the `PATH` contains the Renode installation directory, so the platform files distributed with Renode can be included like so:

```
using "platforms/cpus/miv.repl"
```

You can also provide an absolute path:

```
using "/tmp/platform.repl"
```

Or a path relative to the REPL file that contains the `using` statement:

```
using "./platform.repl"
using "../other/platform.repl"
```

:::{note}

On Windows, `/` can be used as a path separator in all of these cases.
If you want to use Windows-style `\` separators, you will need to escape them:

```
using "D:\\platforms\\platform1.repl"
```
:::
