# CAN integration

```{note}
This feature is available on Linux only.
```

Renode can connect to a virtual CAN interface on the host machine by using an internal SocketCAN bridge.
This integration relies on [SocketCAN](https://www.kernel.org/doc/html/latest/networking/can.html) for the communication between the host and internal CAN networks.

Using this standardized communication method allows Renode to transfer Classical and FD CAN frames. XL CAN frames are handled by the bridge, but they won't be forwarded to the internal network, as this frame type is not yet supported in Renode.

To see CAN host-integration in action, you can try the [SocketCAN bridge demo](https://github.com/renode/renode/tree/master/scripts/complex/socketcan_bridge).

## Host requirements

The bridge relies on SocketCAN to connect to a CAN interface, which includes native, virtual and SLCAN based interfaces.
The examples below assume use of a virtual CAN interface, for which drivers are implemented in the `vcan` kernel module.
To ensure that the module is present in the host, load it with:

```text
$ sudo modprobe vcan
```

To create and set up a virtual network interface named `vcan0`, run:

```text
$ sudo ip link add dev vcan0 type vcan
$ sudo ip link set up vcan0
```

```{note}
Depending on the Linux distribution, the `vcan` module may not be included, or it may not support FD and/or XL CAN frames.
```

## Creating a SocketCAN bridge

A SocketCAN bridge connects to an already existing CAN interface whose name can be provided as a `canInterfaceName` argument.
If not provided, Renode will try to connect to the interface named `vcan0`.

In the simulation the bridge can be connected to internal networks as described in {ref}`CAN-based connections <can-based-connections>`.

By default, Renode will try to enable handling of FD and XL CAN frames, but it won't require them.
To force the use of a specified type, set the optional arguments `ensureFdFrames` and `ensureXlFrames` to `true`.
By setting those, regardless of the creation method, the command or a platform construction will fail if the ensured frame type cannot be enabled.

```{warning}
Be careful about creating a cycle in your CAN network topology.

The frames sent from one bridge can be received by another bridge via the common vcan interface.
If those two bridges are part of the same network, then an infinite loop of packets may be created.
```

### In the Monitor

As mentioned above, there are two ways of creating a `SocketCANBridge`.
The first option is to use the `CreateSocketCANBridge` command.

For example, the following command will create a `SocketCANBridge` named `socketcan`, that connects to the `vcan1` interface and will fail if handling FD frames is not possible.

```text
(machine-0) machine CreateSocketCANBridge "socketcan" "vcan1" ensureFdFrames=true
```

The bridge can be connected to CAN bus as described in {ref}`CAN-based connections <can-based-connections>`.

### In the platform description

Another option is to add a SocketCAN bridge declaration to a `repl` file.
The following example presents a snippet that sets all the arguments of a `socketcan` instance of the `SocketCANBridge` with default values.

```text
socketcan: CAN.SocketCANBridge @ sysbus
    canInterfaceName: "vcan0"
    ensureFdFrames: false
    ensureXlFrames: false
```

The bridge can be connected to CAN bus as described in {ref}`CAN-based connections <can-based-connections>`.
