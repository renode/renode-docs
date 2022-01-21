.. _sharing-files:

Sharing files between host and simulated platform
=================================================

Renode has 3 main methods of file sharing between the guest and the host:

1. built-in TFTP server,
2. Virtio,
3. :ref:`file transfer via the TAP interface <host-network>`.

Tutorial on TAP-based transfers can be found in :ref:`the chapter on host-guest networking <host-network>`.
To achieve the best performance and portability it is recommended to use TFTP or Virtio.

Sharing files using TFTP
------------------------

TFTP (Trivial File Transfer Protocol) is a protocol that allows file transfer between a client and a remote host. Advantages of using TFTP to share files in Renode:

* simplicity,
* configuration doesn't require any interference in machine structure,
* everything can be done in the Monitor,
* does not require host integration, works on all host platforms.

Having a built-in TFTP server in Renode allows you not only to transfer files, but also to easily verify the correctness of your network stack in a deterministic simulated environment.

Starting the TFTP server
++++++++++++++++++++++++

To configure TFTP in Renode you need to create a :ref:`switch and connect it to your machine <wired-network>`.

Now you can create the TFTP server and connect it to your switch::

    emulation CreateNetworkServer "server" "192.168.100.100"
    connector Connect server switch
    server StartTFTP 69

.. note::

    Port 69 is a default for the TFTP protocol, but you can provide any other number acceptable for your TFTP client.

After you successfully start the server, you can access it in the Monitor via ``server.tftp``

Using the TFTP server
+++++++++++++++++++++

Single files can be shared via the TFTP server using the ``ServeFile`` command.

``ServeFile`` accepts two parameters.
The first parameter is a path to your host file and the second parameter is the name under which you expose it via TFTP::

    server.tftp ServeFile @path/to/file "filename"

.. note::

    The second parameter is optional and if it is not specified, the file will be exposed with its original name.

Similarly, you can share directories via TFTP using ``ServeDirectory``::

    server.tftp ServeDirectory @path/to/directory

.. note::

    Keep in mind that the built-in TFTP server does not handle uploading files from the guest to the host.

Sharing files using Virtio
--------------------------

Virtio is a widely used standard for virtualized devices supported in modern OSes.
Advantages of using Virtio to share files in Renode:

* ubiquity of drivers available for various guest OSes,
* support for the MMIO-based Virtio block device model,
* no need for having a platform-specific network controller modeled in Renode,
* faster transfer compared to simulated network transfers.

To use Virtio you need to prepare the filesystem image and fill it with the resources of your choice.
Start by preparing a directory with files you want to constitute your filesystem.

On Linux you can create a filesystem with::

    $ truncate drive.img -s 128MB
    $ mkfs.ext4 -d your-directory drive.img

Then you need to add the Virtio device support to the simulated Linux and the virtual platform in Renode.

.. note::

    Since Linux v2.6.25 Virtio drivers are supported and should be enabled by default (check the CONFIG_VIRTIO and CONFIG_VIRTIO_BLK configuration options).

To enable Virtio, add a device tree entry describing device bus location and interrupt configuration::


    virtio@100d0000 {
        compatible = “virtio,mmio”;
        reg = <0x100d0000 0x150>;
        interrupt-parent = <&plic>;
        interrupts = <42>;
    };

Now you need to add a corresponding extension to the Renode platform definition (the ``.repl`` file)::

    virtio: Storage.VirtIOBlockDevice @ sysbus 0x100d0000
        IRQ -> plic@42

.. note::

    Addresses and interrupt line number must be consistent across ``.repl`` and DTS.

You can set up an underlying image for the Virtio block device by using::

    virtio LoadImage @drive.img

By default, Renode loads the image in a non-persistent mode. If you want to make the Virtio device persistent add the ``true`` argument at the end of the command::

    virtio LoadImage @drive.img true

You can use standard tools like ``dd`` or ``mount`` the device to get access to it.
By default, the VirtIO device is listed in the emulated Linux as ``/dev/vda``.
