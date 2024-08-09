(state-saving)=

# State saving and loading

Renode allows you to save the state of the emulation to a file.

Such a file can be transferred to another user and then loaded to fully recreate the original setup.
No additional binaries or configuration files are required.

To save the emulation state to a file called `statefile.save`, run:

```none
(monitor) Save @statefile.save
```

This file can be used with the `Load` command:

```none
(monitor) Load @statefile.save
```

Or you can load it when starting Renode directly from CLI:

```sh
$ renode statefile.save
```

It is important to remember that a state file created on one version of Renode may not be compatible with another one.

Please note that loading the state file clears the current emulation, and is equivalent to:

```none
(monitor) Clear
(monitor) Load @statefile.save
```

````{note}
After the state is loaded, you must manually set the Monitor's context and reopen the UART windows:

```none
(monitor) mach set 0
(machine-0) showAnalyzer sysbus.uart
```
````

## State saving in tests

It's possible to use the state saving and loading mechanism when defining complex Robot tests.
For details see the {ref}`Test cases dependencies <robot-dependencies>` section.

## Loading gzip compressed save files

Renode also supports loading snapshots compressed with gzip.

You can load them the same way as regular save files:

```none
(monitor) Load @statefile.save.gz
```

Or directly from CLI:

```sh
$ renode statefile.save.gz
```
