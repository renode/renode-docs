# Connecting to the host network

Renode allows you to connect a host network interface to [a simulated wired network](./wired.md).

To do that you need to create a `Tap` interface or `VMNET` interface based on vmnet-helper (the latter is supported only on macOS).

## Regarding time flow

All devices simulated in Renode operate in [virtual time](../advanced/time_framework.md), which is typically slower than the real time flow.
Moreover, network packets are delivered in periodical synchronisation points, delaying the communication even further.

This means that time constraints (e.g. timeouts) placed by applications trying to connect to the simulated network from the host may need to be altered to take these delays into account.

## Opening a TAP interface

To create and open a TAP interface which will be listed on your host system as `tap0` and inside Renode as `host.tap`, run:

```none
(monitor) emulation CreateTap "tap0" "tap"
```

If you want the interface to be retained after Renode closes, add a `true` parameter:

```none
(monitor) emulation CreateTap "tap0" "tap" true
```

Depending on your system configuration, you may be asked for a password to open the interface.

:::{note}
The newly created interface needs to be enabled and configured on your host machine.

By default it has no IP address assigned and is in `down` state.

Please refer to your system documentation for further instructions.
:::

## Using TAP interface on Windows

In order to create a TAP device on Windows, you need to install a third-party driver that is a part of the [OpenVPN project](https://openvpn.net/community-downloads/).
If OpenVPN is installed on your computer, Renode should detect it when trying to create a TAP interface.
The feature has been specifically tested with `OpenVPN 2.5.6`.

:::{note}
You need Administrator Privileges to create a TAP on Windows.
:::

To create a TAP interface on your Windows PC, first, you need to create a new TAP interface in Renode using the usual command:

```none
(monitor) emulation CreateTap "tap0" "tap"
```

Then you need to assign an IP address to your TAP using the command prompt:

```none
netsh interface ipv4 set address name=tap0 static X.X.X.X
```

:::{note}
You can also create a TAP interface directly using the `tapctl.exe` driver from OpenVPN:

```none
tapctl.exe create --name tap0
```

Then assign it an IP address:

```none
netsh interface ipv4 set address name=tap0 static X.X.X.X
```

Finally, connect it to Renode using:

```none
(monitor) emulation CreateTap "tap0" "tap"
```
:::

## Connecting TAP interface to a switch

Assuming you have already [configured the simulated network](./wired.md), you can connect a TAP interface to a `switch` device by running:

```none
(monitor) emulation CreateSwitch "switch"
(monitor) connector Connect host.tap switch
```

## Using VMNET interface on macOS

### Preparing `vmnet-helper`
Before setting up the interface in Renode, install the `vmnet-helper` program by running the following command:

```sh
brew install nirs/vmnet-helper/vmnet-helper
```
or, if you’re on a macOS version earlier than 26, run:

```sh
curl -fsSL https://github.com/nirs/vmnet-helper/releases/latest/download/install.sh | bash
```

### Starting `vmnet-helper`

VMNET configuration consists of three steps:
1. Spawning a background `vmnet-helper` process:
  
   ```sh
   vmnet_helper \
          --socket=${SOCKET_PATH:-vmnet_helper.sock} \
          --operation-mode=${mode:-shared} \
          --start-address=${start_ipv4:-172.16.0.0} \
          --end-address=${end_ipv4:-172.16.0.10} \
          --subnet-mask=${mask:-255.240.0.0}
   ```
   where:
    * `start-address`: the IP address assigned to the host-side interface. This address also acts as the default gateway for the guests.
    * `end-address`: the last IP address in the DHCP pool available for the guests.
    * `subnet-mask`: the subnet mask defining the network size in dotted decimal notation (e.g. 255.255.255.0). The subnet mask enables vmnet to communicate with other vmnet interfaces on the same subnet that are in `shared` mode.
    * `operation-mode`:
      * `host` creates an isolated network where the guest (the VM inside the Renode simulation) can communicate with the host (your computer) but with no access to the Internet. You can use this mode to increase security and privacy.
      :::{note}
      The `--start-address`, `--end-address`, and `--subnet-mask` options are ignored in `host` operation mode in each version of `vmnet-helper` prior to **v0.12.0**.
      :::
      * `shared` where the VM reaches the Internet through a network address translator (NAT) and the host's IP address.
    * For full instructions on using the `vmnet-helper` process, refer to its [README](https://github.com/nirs/vmnet-helper/blob/main/README.md).

:::{note}
All provided IP addresses cannot be arbitrary; they must belong to the private IP address ranges defined by [RFC 1918](https://datatracker.ietf.org/doc/html/rfc1918)
:::

2. Connecting Renode to the `vmnet-helper` process via a Monitor command:
  
   ```none
   emulation CreateVmnetHelper "${SOCKET_PATH}" "vmnet"
   ```

3. Connecting the machine interface and `host.vmnet` to the same switch to allow packet transmission between them:

   ```none
   emulation CreateSwitch "switch"
   connector Connect host.vmnet switch
   connector Connect gem0 switch # use your platform's interface name instead of `gem0`
   ```

If the guest runs Linux, you can test Internet connectivity in the following way:

```sh
ifconfig eth0 up $(($start_ip+1)) # assign any address available in the pool (e.g. the first available address)
ping -c 5 ${start_ip} # any address accessible via the vmnet_helper interface (i.e. your local computer)
```

## Connecting VMNET interface to a switch

Assuming you have already [configured the simulated network](./wired.md), you can connect the VMNET interface `vmnet1` to the `switch` device by running:

```
(monitor) emulation CreateSwitch "switch"
(monitor) connector Connect host.vmnet1 switch
```

## Starting the interface

The TAP and VMNET interfaces are created as "paused".
To enable communication with the host system you must start it manually, either by running:

```none
(monitor) start
```

or, if your emulation is already started, with:

```none
(monitor) host.tap Start
```
```none
(monitor) host.vmnet Start
```

## Transferring files from host

If you successfully created a TAP interface, files can be transferred from the host computer to emulation using `wget`.
To do it you will need to use an IP address associated with the TAP interface on the host machine, for example:

```none
wget http://192.168.100.1/home/user/file.txt
```

:::{note}
There are other methods of file transfer: [built-in TFTP server and Virtio](../host-integration/sharing-files.md).
Those methods are recommended if you want to avoid the limitations of the host-guest networking via TAP.
:::
