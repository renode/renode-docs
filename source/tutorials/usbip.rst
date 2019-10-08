.. _usbip:

USB/IP support
==============

Renode provides a built-in USB/IP server and allows you to export virtual USB devices to the external world.

Exported devices can be attached to the host machine and from that moment the interaction with them
is the same as with real hardware.

This allows for a hybrid setup where part of the system (i.e., virtual USB device and its environment)
is simulated in Renode and the rest comes from the real world.

USB/IP protocol
---------------

The USB/IP protocol allows to share USB devices between a server (exporting party) and a client (importing party)
over the IP network.

The protocol is `well supported in Linux <https://github.com/torvalds/linux/tree/master/tools/usb/usbip>`_, and there exists
a `corresponding project for Windows as well <https://github.com/cezuni/usbip-win>`_, the latter however has not been tested.

Renode currently works as a server only - it is able to support exporting devices only, but is *not able* to
connect physical USB devices to the emulation.

Creating a USB/IP server
------------------------

In order to create a USB/IP server instance in Renode, type the following in the Monitor::

    (monitor) emulation CreateUSBIPServer

As a result a ``host.usb`` device is created in the emulation and the server
is started.

Now you can connect to it from your host machine.
First, you need to import the ``vhci_hcd`` kernel module::

    $ sudo modprobe hvci_hcd

Now, you can list exported devices::

    $ sudo usbip list -r 127.0.0.1
    usbip: info: no exportable devices found on 127.0.0.1

The output above informs that Renode is not exporting any devices at the moment.

Exporting devices
-----------------

Let's export a simple USB device - e.g. a mouse::

    (monitor) host.usb AttachUSBMouse

.. note::

    Note that there are some helper methods allowing to easily attach simple USB devices
    like mouse, keyboard or pendrive directly from ``host.usb``. For more advanced scenario
    see :ref:`foboot_usbip`.

List exported devices again::

    $ sudo usbip list -r 127.0.0.1
    Exportable USB devices
    ======================
    - 127.0.0.1
            1-0: unknown vendor : unknown product (0000:0000)
            : /renode/virtual/1-0
            : (Defined at Interface level) (00/00/00)
            :  0 - Human Interface Device / Boot Interface Subclass / Mouse (03/01/02)

Attaching exported device to host
---------------------------------

The next step is to attach the exported virtual USB device to the host machine::

    $ sudo usbip attach -r 127.0.0.1 -d 1-0

Note that the ``-d`` argument must match the device id returned by the ``usb list`` command.

A new USB mouse should be now visible in the host.
Confirm it by reading the system logs::

    $ sudo dmesg
    ...
    [1310770.549767] usb 7-1: New USB device found, idVendor=0000, idProduct=0000, bcdDevice= 0.00
    [1310770.549771] usb 7-1: New USB device strings: Mfr=0, Product=0, SerialNumber=0
    [1310770.560676] input: HID 0000:0000 as /devices/platform/vhci_hcd.0/usb7/7-1/7-1:1.0/0003:0000:0000.002D/input/input66
    [1310770.560888] hid-generic 0003:0000:0000.002D: input,hidraw4: USB HID v0.00 Mouse [HID 0000:0000] on usb-vhci_hcd.0-1/input0

Or with ``lsusb``::

    $ lsusb -v -d 0000:0000

    Bus 007 Device 091: ID 0000:0000
    Device Descriptor:
    bLength                18
    bDescriptorType         1
    bcdUSB               2.00
    bDeviceClass            0
    bDeviceSubClass         0
    bDeviceProtocol         0
    bMaxPacketSize0        64
    idVendor           0x0000
    idProduct          0x0000
    bcdDevice            0.00
    iManufacturer           0
    iProduct                0
    iSerial                 0
    bNumConfigurations      1
    Configuration Descriptor:
        bLength                 9
        bDescriptorType         2
        wTotalLength       0x0022
        bNumInterfaces          1
        bConfigurationValue     1
        iConfiguration          0
        bmAttributes         0x00
        (Missing must-be-set bit!)
        (Bus Powered)
        MaxPower                0mA
        Interface Descriptor:
        bLength                 9
        bDescriptorType         4
        bInterfaceNumber        0
        bAlternateSetting       0
        bNumEndpoints           1
        bInterfaceClass         3 Human Interface Device
        bInterfaceSubClass      1 Boot Interface Subclass
        bInterfaceProtocol      2 Mouse
        iInterface              0
            HID Device Descriptor:
            bLength                 9
            bDescriptorType        33
            bcdHID               0.00
            bCountryCode            0 Not supported
            bNumDescriptors         1
            bDescriptorType        34 Report
            wDescriptorLength      46
            Report Descriptors:
            ** UNAVAILABLE **
        Endpoint Descriptor:
            bLength                 7
            bDescriptorType         5
            bEndpointAddress     0x81  EP 1 IN
            bmAttributes            3
            Transfer Type            Interrupt
            Synch Type               None
            Usage Type               Data
            wMaxPacketSize     0x0004  1x 4 bytes
            bInterval              10

Now you can control your mouse from Renode.
Type::

    (monitor) host.usb MoveMouse 100 100

and observe the cursor moving on the screen.

.. _foboot_usbip:

Real life scenario: Foboot
--------------------------

In this section we will show how to run a simulation of `Foboot: The Bootloader for Fomu <https://github.com/im-tomu/foboot>`_.

Foboot runs on the Fomu platform that uses the ValentyUSB core to implement a software-driven USB
device where the whole logic (including generating USB descriptors) is executed by the CPU.

Create a Fomu platform
++++++++++++++++++++++

Renode comes with a definition of the Fomu platform.
To create a new virtual Fomu instance, type in the Monitor::

    (monitor) mach create
    (machine-0) machine LoadPlatformDescription @platforms/cpus/fomu.repl

Load the Foboot software::

    (machine-0) sysbus LoadELF @https://antmicro.com/projects/renode/fomu--foboot.elf-s_112080-70b1181d470646a31ebef7300fc8e6dc5447e282

Create a USB/IP server and export Fomu::

    (machine-0) emulation CreateUSBIPServer
    (machine-0) host.usb Register sysbus.valenty

Start the emulation::

    (machine-0) start

Use it on your host machine
+++++++++++++++++++++++++++

Import Fomu on the host::

    $ sudo usbip attach -r 127.0.0.1 -d 1-0

Upload software using ``dfu-util``::

    $ wget https://antmicro.com/projects/renode/fomu--test_binary_flash.bin-s_1016-4a3c37baf69aeb401f834521b0ac4bc6d157ecdf -O fomu--test_binary_flash.bin
    $ sudo dfu-util -D fomu--test_binary_flash.bin
    dfu-util 0.9

    Copyright 2005-2009 Weston Schmidt, Harald Welte and OpenMoko Inc.
    Copyright 2010-2016 Tormod Volden and Stefan Schmidt
    This program is Free Software and has ABSOLUTELY NO WARRANTY
    Please report bugs to http://sourceforge.net/p/dfu-util/tickets/

    dfu-util: Invalid DFU suffix signature
    dfu-util: A valid DFU suffix will be required in a future dfu-util release!!!
    Opening DFU capable USB device...
    ID 1209:5bf0
    Run-time device DFU version 0101
    Claiming USB DFU Interface...
    Setting Alternate Setting #0 ...
    Determining device status: state = dfuIDLE, status = 0
    dfuIDLE, continuing
    DFU mode device DFU version 0101
    Device returned transfer size 1024
    Copying data from PC to DFU device
    Download	[=========================] 100%         1016 bytes
    Download done.
    state(7) = dfuMANIFEST, status(0) = No error condition is present
    state(8) = dfuMANIFEST-WAIT-RESET, status(0) = No error condition is present
    Done!

Disconnect ``dfu-util`` to reboot into the uploaded software::

    $ sudo dfu-util -e

As Fomu does not have many interfaces we can observe, the uploaded binary is quite trivial.
Looking through the log you will see repeated writes of consecutive values to 0x40000000.

To analyze the loaded binary in more detail you can use Renode's :ref:`GDB debugging capabilities <gdb-debugging>` or extensive :ref:`logging support <using-logger>`.
