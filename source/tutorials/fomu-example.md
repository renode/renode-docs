# Renode, Fomu and EtherBone bridge example

This tutorial shows how to run a hybrid simulation where part of the platform is run in Renode and part on FPGA hardware.

## System architecture

The system architecture consists of three main parts:

* [FOMU](https://github.com/im-tomu/fomu-hardware) - Lattice iCE40UP5K-based board with RGB LED, connected to the host machine over USB;
* EtherBone bridge, translating wishbone packets between TCP and USB;
* Renode simulating the [LiteX](https://github.com/enjoy-digital/litex) platform, running Zephyr OS that controls the RGB LED.

## Prerequisites

### Simulation

For the simulation part, you need to have the latest version of Renode available in your system.

You can install [a prebuilt package for your OS](https://github.com/renode/renode/releases) or build a copy from sources as specified in the {doc}`../advanced/building_from_sources`.

### Hardware

For the hardware part, you need to have the [FOMU](https://github.com/im-tomu/fomu-hardware) board.

[FOMU](https://github.com/im-tomu/fomu-hardware) needs to be flashed with the [Foboot](https://github.com/im-tomu/foboot) bitstream containing the [ValentyUSB](https://github.com/mithro/valentyusb) IP core with a USB-Wishbone bridge.
The manufactured FOMU comes preloaded with this bitstream and can be used right away.

If you have assembled your own copy of the board or changed the original bitsteam, please remember to load Foboot again.
For convenience, the prebuilt version of the bitstream is [hosted by Antmicro](https://antmicro.com/projects/renode/foboot-bitstream.bin-s_104250-fc5f419372eb9a3a0baa5556483163bcfccb7d33).

### EtherBone bridge

In order to connect Renode to [FOMU](https://github.com/im-tomu/fomu-hardware) you need to download the EtherBone-to-USB bridge shipped with [LiteX](https://github.com/enjoy-digital/litex).

Clone the repository and initialize the environment:

```bash
git clone https://github.com/enjoy-digital/litex
cd litex
./litex_setup.py init  # this will clone the dependencies
export PYTHONPATH=`pwd`:`pwd`/litex:`pwd`/migen
```

`litex_server.py` additionally requires the `pyusb` package to be installed in the system:

```bash
pip3 install pyusb
```

## Verifying the device

Plug [FOMU](https://github.com/im-tomu/fomu-hardware) into a USB port and verify if it has been recognized by checking the `dmesg` logs:

```text
[65038.250957] usb 2-1: new full-speed USB device number 16 using xhci_hcd
[65038.409283] usb 2-1: New USB device found, idVendor=1209, idProduct=5bf0, bcdDevice= 1.01
[65038.409286] usb 2-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[65038.409287] usb 2-1: Product: Fomu DFU Bootloader v1.7.2-3-g9013054
[65038.409288] usb 2-1: Manufacturer: Foosn
```

Note: The version of the product might differ, but it should work correctly with v.1.7.2 upwards.

If the device is not detected, see the section below.

## Loading the bitstream (optional)

If your device is detected as a DFU Bootloader in version 1.7.2 or higher, you can skip this step.

In order to upload a bitstream to a device that is not recognized as a DFU Bootloader you will need an external programming board.

:::{note}

For convenience, you can use [the Fomu Programmer](https://github.com/antmicro/fomu-programmer) - the Open Hardware programming board for [FOMU](https://github.com/im-tomu/fomu-hardware) by Antmicro.

:::

Download and make [iceprog](https://github.com/cliffordwolf/icestorm/tree/master/iceprog) - open source programming software for Lattice iCE40:

:::{note}

Building `iceprog` requires the `ftdi` library headers to be available in the system.

:::

```bash
git clone https://github.com/cliffordwolf/icestorm
cd icestorm/iceprog
make
```

Download the prebuilt bitstream:

```bash
wget https://antmicro.com/projects/renode/foboot-bitstream.bin-s_104250-fc5f419372eb9a3a0baa5556483163bcfccb7d33 -O foboot-bitstream.bin
```

:::{note}

You can also build the bitstream yourself by following the instructions on the [Foboot](https://github.com/im-tomu/foboot) page.

:::

Attach the board to the programmer and load the bitstream to the FPGA:

```bash
sudo iceprog foboot-bitstream.bin
```

## Running the demo

Start the EtherBone bridge from the [LiteX](https://github.com/enjoy-digital/litex) repository:

```bash
cd litex
sudo python3 litex/tools/litex_server.py --usb --usb-vid 0x1209 --usb-pid 0x5bf0
```

Run the Zephyr OS image in simulation using the script shipped with Renode:

```text
(monitor) start @scripts/complex/fomu/renode_etherbone_fomu.resc
```

Now you can control the HW LED from Zephyr's shell using special commands:

```bash
uart:~$ led_toggle
uart:~$ led_breathe
```

`led_toggle`
    toggles the green led

`led_breathe`
    makes the blue led blink with a fade-in/fade-out effect

