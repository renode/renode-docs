# Using Renode

## Running and quitting Renode

To start Renode, use the `renode` command in your operating system's terminal.

The current terminal will now contain the Renode log window, and a new window will pop up for "the Monitor" - the CLI for Renode.

To quit Renode gracefully and close all the associated windows, use the `quit` command in the Monitor at any time.

(monitor)=

## Monitor (Renode CLI)

The Monitor is used to interact with Renode and control the emulation.
It exposes a set of basic commands and allows the user to access emulation objects.
Using the Monitor, the user can execute actions provided by those objects as well as examine and modify their state.

The Monitor comes with several built-in features to make the user experience similar to a regular terminal application.

### Using built-in commands

The `help` command provides a list of available built-in commands with a short description:

```none
(monitor) help
Available commands:
Name              | Description
================================================================================
alias             : sets an alias.
allowPrivates     : allow private fields and properties manipulation.
analyzers         : shows available analyzers for peripheral.
commandFromHistory: executes command from history.
createPlatform    : creates a platform.
currentTime       : prints out and logs the current emulation virtual and real time
...
```

You can get more detailed information about a selected command by using the `help` command with another built-in command as an argument:

```none
(monitor) help analyzers
Usage:
------
analyzers [peripheral]
 lists ids of available analyzer for [peripheral]
analyzers default [peripheral]
 writes id of default analyzer for [peripheral]
```

Typing any command with wrong or incomplete arguments will also print a help string.

For ease of use, a partial autocompletion feature is available.
Just press <kbd>Tab</kbd> once to complete the current command or twice to see all available suggestions.

For commands with file arguments, the `@` sign represents a path to a file; for convenience, Renode also provides autocompletion for filenames.

```{note}
After a `@` sign, the Monitor will suggest files both in the current working directory from which Renode was run and in the Renode installation directory as a fallback - the former taking precedence in case of ambiguity.
For non existing files the Renode directory takes precedence. If you want to create a file in your local directory, use the ``$CWD`` variable or provide a full path.
```

The most common commands (e.g., `start` or `quit`) provide short, usually single-letter, aliases (so `s` and `q`, respectively).

The CLI provides a command history (arrows <kbd>↑</kbd>/<kbd>↓</kbd>) with interactive search <kbd>Ctrl</kbd>+<kbd>R</kbd> to easily re-execute previous commands.

Pasting with <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd>, as well as via the context menu on right click, is also available.
To erase the current command and return to a clean prompt, use: <kbd>Ctrl</kbd>+<kbd>C</kbd>.

## Basic interactive workflow

When running Renode interactively, the user would normally start by {ref}`creating the emulation <working-with-machines>` through a sequence of commands building up, configuring, and connecting the relevant emulated (guest) platform or platforms (called "machines").

This is normally done using nested {ref}`scripts` which help encapsulate some of the repeatable elements in this activity (normally, the user will want to create the same platform over and over again in between runs, or even script the execution entirely).

When the emulation is created and all the necessary elements (including e.g. binaries to be executed) are loaded, the emulation itself can be started - to do this, use the `start` command in the Monitor.

At this point, you will be able to see lots of information about the operation of the emulated environment in the [logger window](../basic/logger.md), extract additional information and manipulate the running emulation using the Monitor (or plugins such as [Wireshark](../networking/wireshark.md) - as well as interact with the external interfaces of the emulated machines like UARTs or [Ethernet controllers](../networking/wired.md).

For some typical commands useful in creating and manipulating machines from the Monitor, you can refer to the {ref}`working-with-machines` section.

Some more commands and info on interacting with the emulation can be found in the {ref}`basic-control` section.

(scripts)=

.resc scripts
-------------

Renode scripts (.resc) enable you to encapsulate repeatable elements of your project (like creating a machine and loading a binary) to conveniently execute them multiple times.
The syntax used in `.resc` files is the same as that of the Monitor.

Renode has many built-in `.resc` files, like this [Intel Quark C1000 script](https://github.com/renode/renode/blob/master/scripts/single-node/quark_c1000.resc).

To load it in Renode, use the ``include`` command with a path:

```
include @scripts/single-node/quark_c1000.resc
```

If in the above command you use `start` (or just `s`) instead of `include`, the emulation will start immediately after loading the script.

```{note}
Remember about path autocompletion using the <kbd>Tab</kbd> key after `@`, as described in the {ref}`previous section <monitor>`.
```

Scripts can `include` further scripts, which is useful e.g. to create complex multinode setups like in the [nRF52840 BLE demo](https://github.com/renode/renode/blob/master/scripts/multi-node/nrf52840-ble-zephyr.resc).

[Built-in Renode demo scripts](https://github.com/renode/renode/tree/master/scripts) are a great entry point - to run your first demo, proceed to the {doc}`demo` chapter.

## Configuring the user interface

The appearance of the user interface can be customized via the user configuration file `config`.
It is located in the directory `~/.config/renode` on Unix-like systems and in `AppData\Roaming\renode` on Windows.

In the section `[termsharp]`, the following settings are available:
  
| Name            | Description                                                                                                                                        |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| append-CR-to-LF | This setting controls if a carriage return is appended to each line feed.<br>Allowable values are `true` and `false`. The default value is `true`. |
| font-face       | Name of the TrueType font used in the log and monitor windows.<br>The default value is `Roboto Mono`.                                              |
| font-size       | Font size in points. The default value is 12 on Windows and 10 on Linux.                                                                           |
| window-width    | Initial width (in pixels) of the log and monitor windows.                                                                                          |
| window-height   | Initial height (in pixels) of the log and the monitor windows.                                                                                     |
