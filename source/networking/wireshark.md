# Inspecting the traffic with Wireshark

[Wireshark](https://www.wireshark.org) is an open source network packet analyzer that can be used to sniff the network traffic between emulated nodes and/or the host network interface.

Renode uses the libpcap format to provide data to Wireshark.

## Logging the whole traffic

Renode supports multiple link layer protocols, i.e. Ethernet, Bluetooth Low Energy and IEEE 802.15.4.
Each protocol has its own set of commands to enable logging of all traffic or with filtering.

The `emulation Log<Protocol Name>Traffic` commands will automatically connect Wireshark to all existing and new networks for the given protocol.

```{list-table} Protocol specific global logging
:header-rows: 1

* - Protocol
  - Command
* - Ethernet
  - LogEthernetTraffic
* - Bluetooth Low Energy
  - LogBLETraffic
* - IEEE 802.15.4
  - LogIEEE802_15_4Traffic
```

You can also manually open Wireshark window, before setting up a network with:

```text
(monitor) host.wireshark-all<Protocol Name>Traffic Run
```

## Observing a specific interface

Inspecting traffic of a specific switch or a wireless medium can be done with `emulation LogToWireshark` command.
You can also limit the observation to a specific interface connected to that switch or medium.


```{list-table} Protocol specific filtered logging
:header-rows: 1

* - Protocol
  - Interface type
* - Ethernet
  - Switch
* - Bluetooth Low Energy
  - BLEMedium
* - IEEE 802.15.4
  - IEEE802_15_4Medium
```

### Ethernet example

To enable logging on a `switch` object run:

```text
(monitor) emulation LogToWireshark switch
```

To observe only the `sysbus.ethernet` interface connected to `switch` run:

```text
(machine-0) emulation LogToWireshark switch sysbus.ethernet
```

The names of Wireshark objects created depend on the machine name, the switch name and the interface name.
In the above case Renode creates an object named `host.wireshark-switch-machine-0-sysbus-ethernet`.
