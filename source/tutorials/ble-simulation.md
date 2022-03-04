# Bluetooth Low Energy simulation in Renode

Bluetooth Low Energy is a widespread wireless protocol most commonly used in consumer devices such as blood pressure monitors, wearables, and smart home appliances.
Thanks to its multi-node networking capabilities, Renode can be used to develop and test complete products in those and other areas using BLE.

Renode support for BLE has primarily been developed in the context of the [Zephyr RTOS](https://docs.zephyrproject.org/latest/introduction/index.html) and Nordic's [nRF52840 SoC](https://www.nordicsemi.com/Products/nRF52840).

## Running a precompiled demo

You can start with a precompiled demo which will just run two nodes communicating over BLE. Use the following command in the Monitor to do that:

```
(monitor) include scripts/multi-node/nrf52840-ble-zephyr.resc
```

You should see two serial ports open and packets being sent.

## Building your own Zephyr samples

You can see the full list of Zephyr samples and demos in the [Zephyr documentation](https://docs.zephyrproject.org/latest/samples/index.html) which describes in more detail how to install and use the RTOS.

Here we will focus on some essentials which are specific to this demo.

To build the relevant samples, after [setting up Zephyr as usual](https://docs.zephyrproject.org/latest/getting_started/index.html) you can use the following commands.

```
cd ~/zephyrproject/zephyr
west build -b nrf52840dk_nrf52840 -d central samples/bluetooth/central_hr
cp central/zephyr/zephyr.elf ./zephyr-ble-central_hr.elf

west build -b nrf52840dk_nrf52840 -d peripheral samples/bluetooth/peripheral_hr
cp peripheral/zephyr/zephyr.elf ./zephyr-ble-peripheral_hr.elf
```

```{note}
If you want to run a new build and remove byproducts of the previous build, you should add `-p auto` parameter to your command.
```

To use these binaries in the demo shipped with Renode, you can override the relevant variables before you load the script:

```
(monitor) $central_bin=@zephyr-ble-central_hr.elf
(monitor) $peripheral_bin=@zephyr-ble-central_hr.elf
(monitor) include scripts/multi-node/nrf52840-ble-zephyr.resc

```

## Looking into the script

Bellow you can find a full example which creates 2 devices that generate and read heart-rate monitor data over BLE:

```
using sysbus

$central_bin?=@zephyr-ble-central_hr.elf
$peripheral_bin?=@zephyr-ble-central_hr.elf

emulation CreateWirelessMedium "wireless"

mach create "central"
machine LoadPlatformDescription @platforms/cpus/nrf52840.repl
connector Connect sysbus.radio wireless

showAnalyzer uart0

mach create "peripheral"
machine LoadPlatformDescription @platforms/cpus/nrf52840.repl
connector Connect sysbus.radio wireless

showAnalyzer uart0

emulation SetGlobalQuantum "0.00001"

macro reset
"""
    mach set "central"
    sysbus LoadELF $central_bin

    mach set "peripheral"
    sysbus LoadELF $peripheral_bin
"""
runMacro $reset

echo "Script loaded. Now start with the 'start' command."
echo ""
```

The script is responsible for creating two machines, opening up their UART analyzers, connecting them in a single network and loading the provided binaries.

The first Renode "machine" - dubbed `central` - runs the [central_hr sample](https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/bluetooth/central_hr) which looks for active heart-rate monitors using BLE and connects to the device with the strongest signal.
The second one - `peripheral` - runs the [peripheral_hr sample](https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/bluetooth/peripheral_hr), which creates a machine that functions as a heart-rate monitor and generates dummy heart-rate values.

When the connection is established, `central` will report data reception from `peripheral`.

To learn more about specific commands, see the {doc}`../basic/machines` chapter and [the comments in the script on the Renode repository](https://github.com/renode/renode/blob/master/scripts/multi-node/nrf52840-ble-zephyr.resc).


## Packet interception hooks with BLE

You can make your simulated machine react to a wireless networking (e.g. BLE) packet appearing on the radio medium by means of a Python hook.
Such a hook hook will execute Python code either directly from the Monitor or from a designated file.
To set up a packet interception hook on the machine from the example above, you would run:

```
(peripheral) wireless SetPacketHookFromScript radio "self.DebugLog('Received a packet of {} bytes'.format(len(packet)))"
```
