# UART integration

Renode enables exposing emulated UART devices to the host machine and interacting with them using the standard workflow (tools, scripts, etc.) exactly as if they were actual hardware serial ports.
This opens the door to designing hybrid setups where part of the system is simulated in Renode and the rest consists of physical devices or software running in the "real world".

Renode provides two independent mechanisms for exposing virtual UART devices to the host machine:

- using a pty device (Linux/macOS only),
- over a network socket (available on all platforms).

You can also redirect UART output to a file, but this is does not allow for reading user input.

## UART pty terminal

:::{note}
This feature is available on Linux/macOS only.
:::

UART pty terminal integration allows creating a pty device in the host filesystem that acts as a bridge between the real world and the simulation.
Data written to/read from the pty device by the software running in the real world is automatically transferred to the virtual UART device (and vice versa).

In order to expose a virtual UART device, create the UART pty terminal with the following command in the Monitor:

```
(monitor) emulation CreateUartPtyTerminal "term" "/tmp/uart"
```

This will create a new file in the host filesystem (`/tmp/uart`) that can be referenced from within the simulation as `term`.

Now you need to [load your platform](#loading-platforms) and connect the newly created UART pty terminal to the simulated UART device:

```
(machine-0) connector Connect sysbus.uart0 term
```

This assumes your UART is called `sysbus.uart0`, but you might need to adjust it to match your platform.

Finally, open the terminal application on your host machine (`screen`/`picocom`/`PuTTY`/etc.) and attach it to the `/tmp/uart` file.
You can interact with it just like with the hardware.

## Socket terminal

:::{note}
This feature is available on all supported host platforms (Linux/macOS/Windows).
:::

Socket terminal integration allows exposing a virtual UART device over a network socket and making it available for any device in the network.
The data sent to the socket available on a selected port number by the software running in the real world (on the local host machine or over the network) is automatically transferred to the virtual UART device (and vice versa).

In order to expose a virtual UART device, create a Socket terminal with the following command in the Monitor:

```
(monitor) emulation CreateServerSocketTerminal 12345 "term"
```

This will open a tcp network port `12345` on the host machine that can be referenced from within the simulation as `term`.

Now, connect the newly created Socket terminal to the simulated UART device:

```
(machine-0) connector Connect sysbus.uart0 term
```

Finally, open the terminal application on your host machine (`netcat`/`telnet`/`PuTTy`/etc.) and connect it to port 12345.
You can interact with it just like with the hardware.

### Emitting configuration bytes

By default Server Socket will emit the following initial configuration bytes in order to properly configure a newly connected terminal:

```
0xff, 0xfd, 0x00, // IAC DO    BINARY
0xff, 0xfb, 0x01, // IAC WILL  ECHO
0xff, 0xfb, 0x03, // IAC WILL  SUPPRESS_GO_AHEAD
0xff, 0xfc, 0x22  // IAC WONT  LINEMODE
```

In order to avoid generating them, pass additional `false` argument when creating the Socket terminal:

```
(monitor) emulation CreateServerSocketTerminal 12345 "term" false
```

## Redirecting to a file

Renode can redirect UART output to a file on your host.
To enable this feature, call:

```
(machine-0) uart CreateFileBackend @uart_file
```

By default, the UART output will be cached by the host IO system.
If you want the output to be flushed immediately after being sent, use:

```
(machine-0) uart CreateFileBackend @uart_file_flush true
```

If you want, you can stop this output with:

```
(machine-0) uart CloseFileBackend @uart_file
```

Keep in mind that subsequent calls to the `CreateFileBackend` method will not overwrite the previous file of the same name, but rather copy, appending a consecutive number to its name.
