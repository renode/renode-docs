# Machine to machine connections

There are various ways of connecting two machines in Renode.
Other than {doc}`wired <wired>` and {doc}`wireless <wireless>` networking (decribed in their own chapters), there are several other interfaces available, divided into two categories:

- {ref}`Symmetrical, like UART or CAN<symmetrical-connections>`,
- {ref}`Asymmetrical, like GPIO or USB<asymmetrical-connections>`.

(symmetrical-connections)=

## Symmetrical connections

In Renode, connections like UART and CAN are always symmetrical, meaning each side can be either the initiator or the recipient of a transfer.
A symmetrical connection is represented by a "hub" object to which the communicating machines need to be connected.

### UART-based connections

To connect two UART devices, you need to create a UART hub, which can be created in the Monitor by executing:

```
(monitor) emulation CreateUARTHub "uartHub"
```

The UART hub created by this line is named `uartHub`, but you can use any name.

Then, you have to connect your UART devices to the common UART hub using the `connector` mechanism:

```
(monitor) mach set 0
(machine-0) connector Connect sysbus.uart uartHub
(machine-0) mach set 1
(machine-1) connector Connect sysbus.uart uartHub
```

To disconnect a device from the `uartHub`, execute:

```
(machine-1) connector Disconnect sysbus.uart uartHub
```

The UART hub is created in a paused state, which means it won't transfer any data between devices.
To enable communication, you must start your hub.

For simplicity, in the default scenario your `uartHub` will start automatically when starting the whole simulation:

```
(monitor) start
```

In case you need to start your `uarthub` manually (e.g. when adding it to a running simulation):

```
(monitor) uartHub Start
```

Now, data sent by `sysbus.uart` on `machine-0` will be received by `sysbus.uart` on `machine-1` and vice versa.

Your hub can be paused at any moment by executing:

```
(monitor) uartHub Pause
```

It can then be resumed using:

```
(monitor) uartHub Resume
```

In order to ensure the determinism of the simulation, bytes sent over an uartHub are buffered and delivered to the receiver at set times.
Please note that this might lead to slight delays in communication.
The maximum delay is controllable by the `quantum` parameter.
For details on how the synchronization works and how to configure it, refer to [the Time framework synchronization section](../advanced/time_framework.md#synchronization) of the documentation.

(can-based-connections)=

### CAN-based connections

Connecting two machines with the CAN bus is very similar to connecting them with a UART.

First, you need to create a CAN hub in the Monitor:

```
(monitor) emulation CreateCANHub "canHub"
```

Then, you have to connect both of your devices to the CAN Hub using the `connector` mechanism:

```
(monitor) mach set 0
(machine-0) connector Connect sysbus.can canHub
(machine-0) mach set 1
(machine-1) connector Connect sysbus.can canHub
```

To disconnect a device from the `CANHub`, execute:

```
(machine-1) connector Disconnect sysbus.can canHub
```

```{note}
Similar to the UART Hub, the CAN Hub can be freely started, paused, and resumed using the same commands.
```

(asymmetrical-connections)=

## Asymmetrical connections

In Renode, GPIO and USB connections are always asymmetrical.
This requires you to specify which machine is the `controller` and which is the `peripheral`.

### GPIO connections

GPIO connections in Renode allow you to send a boolean signal (`true` or `false`) between GPIO pins of two machines.
The `GPIOConnector` object represents a unidirectional GPIO connection with a source and destination, which is why GPIO is listed as an asymmetrical connection method.
However, you can create two `GPIOConnector` objects with reversed source and destination in order to effectively get a bidirectional connection.

To create a `GPIOConnector`, use:

```
(monitor) emulation CreateGPIOConnector "gpio-con"
```

You can connect a maximum of two machines to your `GPIO Connector`, one being `INumber GPIO Output` and the other being `IGPIOReceiver`.
Trying to connect more will always result in an error.

Next, you need to select GPIO pins available in the machines you want to use in the connection.
In the example below, we chose to use pin 7 in the `source` machine and pin 4 in the `destination` machine.

```
(monitor) mach set "source" 
(source) connector Connect sysbus.gpio gpio-con
(source) gpio-con SelectSourcePin sysbus.gpio 7

(monitor) mach set "destination"
(destination) connector Connect sysbus.gpio gpio-con
(destination) gpio-con SelectDestinationPin sysbus.gpio 4
```

```{note}
Keep in mind that the signal can only be sent from the `SourcePin` to the `DestinationPin`.
To create a connection working the other way around, please create another `GPIOConnector`.
```
        
### USB connections

To be able to create a USB connection between two machines in Renode, first, you need to create a `USBConnector`.

```
(monitor) emulation CreateUSBConnector "usb-connector"
```

In this type of connection, your machines are assigned the `device` or `controller` role.
Like in the other connection types, you need to use a `connector` mechanism to connect the `usb-connector` to the USB port on your machine.
Your device then has to be registered in the `controller` device and connected to its USB.

```
(monitor) mach set "device"
(device) connector Connect sysbus.usb usb-connector

(device) mach set "controller"
(controller) usb-connector RegisterInController sysbus.usb-controller
```

## Modeling the timing of the events

Some models require an event to happen at a specified moment in time (e.g. some time after the other event).
To achieve this, you can use various mechanisms:

- implementing a `LimitTimer` in a peripheral, that can execute actions periodically.
  This is used mainly, but not only, for implementing timer logic,
- `machine.LocalTimeSource.ExecuteInNearestSyncedState` to delay an event by some amount of time, which is not clearly specified,
- `machine.LocalTimeSource.ExecuteInSyncedState`, which gives you more control over the specific time at which the event should happen,
- `machine.ObtainManagedThread`, which is the easiest way to execute actions at a specified frequency.

All of these mechanisms are handled by the machine and its time source, so that the logic is hidden from the peripheral model.

More detailed information about the Time framework in Renode can be found in the relevant chapter: {doc}`Time framework <../advanced/time_framework>`.
