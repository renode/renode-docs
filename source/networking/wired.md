# Setting up a wired network

Renode allows you to create complex network topologies using the Monitor.

Both wired and [wireless](./wireless.md) networks can coexist, but are created with different commands.

## Creating a switch

Wired network interfaces can be connected via switches.
Depending on the desired topology, you can create one or more switches and attach interfaces accordingly.

The network traffic is not affected by the number of nodes connected to one switch.

To create a switch named `switch1`, run:

```
(monitor) emulation CreateSwitch "switch1"
```

## Connecting interfaces

To connect an interface to a switch you have to set a proper [machine context](../basic/machines.md#switching-between-machines).

Then, use the `connector` mechanism to attach the interface:

```none
(machine-0) connector Connect sysbus.ethernet switch1
```

Although it is not a common setup, each interface can be connected to many switches at the same time.

## Disconnecting interfaces

You can disconnect network interfaces from a switch by running:

```none
(machine-0) connector Disconnect sysbus.ethernet switch1
```

To disconnect from all connected switches, use:

```none
(machine-0) connector DisconnectFromAll sysbus.ethernet
```

## Starting the interface

A `Switch` object is created as "paused".
To enable communication via a switch you must start it manually, either by running:

```
(monitor) start
```

or, if your emulation is already started, with:

```none
(monitor) switch1 Start
```

## Controlling the traffic

If a packet has a specified destination MAC address, the switch will try to deliver it to the appropriate interface.
If, however, the address is not set or the switch is not aware of an interface with this MAC, the packet is broadcast to all connected interfaces.

You can alter this behavior by enabling promiscuous mode for a specified interface:

```none
(machine-0) switch1 EnablePromiscuousMode sysbus.ethernet
```

After this command, the `sysbus.ethernet` interface will receive all packets delivered to `switch1` from other interfaces.

To disable promiscuous mode, run:

```none
(machine-0) switch1 DisablePromiscuousMode sysbus.ethernet
```
