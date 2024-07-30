# Sharing files between host and simulated platform

Renode has 4 main methods of file sharing between the guest and the host:

1.  VirtIO block device,
2.  directory sharing,
3.  built-in TFTP server,
4.  [file transfer via the TAP interface](../networking/host-network.md).

Tutorial on TAP-based transfers can be found in [the chapter on host-guest networking](../networking/host-network.md).
To achieve the best performance and portability it is recommended to use TFTP or VirtIO.

## Sharing files using VirtIO block device

VirtIO is a widely used standard for virtualized devices supported in modern OSes.
Advantages of using VirtIO to share files in Renode:

- ubiquity of drivers available for various guest OSes,
- support for the MMIO-based VirtIO block and filesystem device model,
- no need for having a platform-specific network controller modeled in Renode,
- faster transfer compared to simulated network transfers.

To use VirtIO block device you need to prepare the filesystem image and fill it with the resources of your choice.
Start by preparing a directory with files you want to constitute your filesystem.

On Linux you can create a filesystem with:

```sh
$ truncate drive.img -s 128MB
$ mkfs.ext4 -d your-directory drive.img
```

Then you need to add the VirtIO block device support to the simulated Linux and the virtual platform in Renode.

:::{note}
Since Linux v2.6.25 VirtIO drivers are supported and should be enabled by default (check the CONFIG_VIRTIO, CONFIG_VIRTIO_MMIO and CONFIG_VIRTIO_BLK configuration options).
:::

To enable VirtIO, add a device tree entry describing device bus location and interrupt configuration:

```dts
virtio@100d0000 {
    compatible = "virtio,mmio";
    reg = <0x100d0000 0x150>;
    interrupt-parent = <&plic>;
    interrupts = <42>;
};
```

Now you need to add a corresponding extension to the Renode platform definition (the `.repl` file):

```
virtio: Storage.VirtIOBlockDevice @ sysbus 0x100d0000
    IRQ -> plic@42
```

:::{note}
Addresses and interrupt line number must be consistent across `.repl` and DTS.
:::

You can set up an underlying image for the VirtIO block device by using:

```
virtio LoadImage @drive.img
```

By default, Renode loads the image in a non-persistent mode. If you want to make the VirtIO block device persistent add the `true` argument at the end of the command:

```
virtio LoadImage @drive.img true
```

You can use standard tools like `dd` or `mount` the device to get access to it.
By default, the VirtIO device is listed in the emulated Linux as `/dev/vda`.

## Directory sharing

Directory sharing functionality is available when using VirtIO filesystem device.

This device enables directory sharing between the guest and host.
Advantages of using this feature:

- real time host and guest file transfer
- no need to restart the machine to upload new files
- no need to repack images or filesystems

### Libfuse

Sharing directory on the host is performed with the use of FUSE filesystem daemon, which handles requests on the directory from Renode.
The shared directory must be a FUSE filesystem connected via a Unix domain socket.
A passthrough filesystem has been prepared to use with this device with use of libfuse library.

### Installation

**Requirements**:

- [Meson](http://mesonbuild.com/)
- [Ninja](https://ninja-build.org/)

Filesystem daemon installation:

```sh
$ git clone https://github.com/antmicro/libfuse --branch passthrough-hp-uds
$ cd renode-filesystem-sharing-libfuse
$ mkdir build; cd build
$ meson setup ..
$ ninja
```

Filesystem daemon binary will be located at `example/passthrough_hp_uds`.
For easier usage, export that binary location to `$PATH`.

### Usage

:::{note}
Virtiofs drivers have been supported in Linux since version 5.4 and should be enabled by default (you can check the CONFIG_VIRTIO_FS config option during compilation).
Remember to include the `virtiofs` device under `soc` in the device tree.
:::

Add a device tree entry describing device bus location and interrupt configuration:

```dts
virtio@100d0000 {
    compatible = "virtio,mmio";
    reg = <0x100d0000 0x150>;
    interrupt-parent = <&plic>;
    interrupts = <0x2>;
};
```

Now you need to add a corresponding extension to the Renode platform definition (the `.repl` file):

```
virtio: Storage.VirtIOFSDevice @ sysbus 0x100d0000
    IRQ -> plic@2
```

:::{note}
Addresses and interrupt line number must be consistent across `.repl` and DTS.
:::

Start the filesystem daemon:

```sh
$ passthrough_hp_uds path_to_share
```

By default, this creates a USD socket in `/tmp/libfuse-passthrough-hp.sock`.

Create the virtiofs device in Renode:

```
virtio Create @/tmp/libfuse-passthrough-hp.sock "tag"
```

with `tag` being a name of your choosing.

In guest you can now mount the shared directory:

```
# mount -t virtiofs tag /mnt
```

## Sharing files using TFTP

TFTP (Trivial File Transfer Protocol) is a protocol that allows file transfer between a client and a remote host. Advantages of using TFTP to share files in Renode:

- simplicity,
- configuration doesn't require any interference in machine structure,
- everything can be done in the Monitor,
- does not require host integration, works on all host platforms.

Having a built-in TFTP server in Renode allows you not only to transfer files, but also to easily verify the correctness of your network stack in a deterministic simulated environment.

### Starting the TFTP server

To configure TFTP in Renode you need to create a [switch and connect it to your machine](../networking/wired.md).

Now you can create the TFTP server and connect it to your switch:

```
emulation CreateNetworkServer "server" "192.168.100.100"
connector Connect server switch
server StartTFTP 69
```

:::{note}
Port 69 is a default for the TFTP protocol, but you can provide any other number acceptable for your TFTP client.
:::

After you successfully start the server, you can access it in the Monitor via `server.tftp`

### Using the TFTP server

Single files can be shared via the TFTP server using the `ServeFile` command.

`ServeFile` accepts two parameters.
The first parameter is a path to your host file and the second parameter is the name under which you expose it via TFTP:

```
server.tftp ServeFile @path/to/file "filename"
```

:::{note}
The second parameter is optional and if it is not specified, the file will be exposed with its original name.
:::

Similarly, you can share directories via TFTP using `ServeDirectory`:

```
server.tftp ServeDirectory @path/to/directory
```

:::{note}
Keep in mind that the built-in TFTP server does not handle uploading files from the guest to the host.
:::
