# Renode testing API

For an introduction to testing with Renode, visit the [Testing with Renode](https://renode.readthedocs.io/en/latest/introduction/testing.html) section of our documentation.

## General methods
We have many methods of accessing a simulation state you can use for testing.
Some of them are Renode commands that you can execute in the robot framework as follows:
```
Execute Command     <renode-command>
```
You can use the following template to extract data out of a simulation:
```
${value}=  Execute Command     <renode-command>
```
To check against conditions with robot keywords, run the commands below:
```
Should Be Equal                ${value}  <expected-value>
Should Be Equal As Numbers     ${value}  <expected-value>
Should Be Equal As Integers    ${value}  <expected-value>
```

### Accessing memory
To access memory at a given address, you can use Renode `Read<Width>` commands as shown below. They enable you to get both memory and peripheral registers content.
```
${value}= Execute Command     sysbus ReadByte        <address>
${value}= Execute Command     sysbus ReadWord        <address>
${value}= Execute Command     sysbus ReadDoubleWord  <address>
${value}= Execute Command     sysbus ReadQuadWord    <address>
```

### Accessing CPU registers
To access a CPU register, use the following command:
```
${val}=  Execute Command        cpu GetRegister <register-name>
```
Alternatively, if you only want to compare a register against an expected value, use:
```
Register Should Be Equal     <register-name>  <expected-value>
```
See the [example test case](https://github.com/renode/renode/blob/master/tests/platforms/Veer_EL2_Timers.robot#L175) for usage.

### Accessing simulation logs
To access simulation logs, first create a log tester:
```
Create Log Tester            <timeout>
```
Then, to verify if an expected log entry appears in the logs, run:
```
Wait For Log Entry           <expected-log>
```

For more details, see the [Log Tester Keywords implementation](https://github.com/renode/renode/blob/master/src/Renode/RobotFrameworkEngine/RenodeKeywords.cs#L330) and the [example test case](https://github.com/renode/renode/blob/master/tests/platforms/ambiq-apollo4.robot#L210).

### Hooks at symbols

Renode enables you to create a hook on a symbol or an address in the form of a Python-scripted breakpoint.

A simple example of a hook is an addition of a log through the following command:
```
Execute Command                 cpu AddHook `sysbus GetSymbolAddress "timerIRQ"` "cpu.ErrorLog('timer interrupt @ {0}', monitor.Machine.ElapsedVirtualTime.TimeElapsed)"
```

You can then assert the hook execution, and therefore symbol execution, as follows:
```
Wait For Log Entry              timer interrupt
```
See the [example test case](https://github.com/renode/renode/blob/master/tests/platforms/Renesas_RA8M1.robot#L147) for usage.

## UART
To verify if a UART outputs correct data, first create a terminal tester and attach it to a selected peripheral:
```
Create Terminal Tester          sysbus.uart
```
Then, use one of the following commands to wait for the expected output:
* Wait until a given line is sent to the UART:
  ```
  Wait For Line On Uart       Expected Line
  ```
* Wait until a given prompt (a line without a newline character) is sent to the UART:
  ```
  Wait For Prompt On Uart     Expected Prompt
  ```
* Wait until a given sequence of bytes is sent to the UART:
  ```
  Wait For Bytes On Uart      59 52 20 4f 53
  ```

You can also interfere with the simulation by sending data to the UART with one of the following commands:
* Send a single character to the UART:
  ```
  Send Key To Uart      0xD
  ```
* Send a line to the UART:
  ```
  Write Line To Uart    Example Line
  ```

For a full list of commands and parameters, see the [Uart Tester Keywords implementation](https://github.com/renode/renode/blob/master/src/Renode/RobotFrameworkEngine/UartKeywords.cs).

The UART testing can also be scripted in Python with [Virtual Console](https://renode.readthedocs.io/en/latest/basic/using-python.html#virtual-console) or automated with file-based feeding using the [UART RESD Feeder](https://renode.readthedocs.io/en/latest/basic/resd.html#uart-resd-feeder).

## GPIO
To verify a GPIO interface, use LEDs and buttons, both of which need to be created first. The easiest way to do it is by using REPL strings. Use the snippet below to connect a LED to the 100th pin of the `gpio` peripheral:
```
${LED_REPL}                         SEPARATOR=\n
...                                 """
...                                 led: Miscellaneous.LED @ gpio 0
...
...                                 gpio:
...                                 ${SPACE*4}100 -> led@0
...                                 """
```
The snippet below connects a button to the 7th pin of the `gpio` peripheral:
```
${BUTTON_REPL}                      SEPARATOR=\n
...                                 """
...                                 button: Miscellaneous.Button @ gpio 1
...                                 ${SPACE*4}-> gpio@7
...                                 """
```
Then, load those snippets in a test case through the following commands:
```
Execute Command                 machine LoadPlatformDescriptionFromString ${LED_REPL}
Execute Command                 machine LoadPlatformDescriptionFromString ${BUTTON_REPL}
```

To check the GPIO state on the pin on which you created the LED, first create a LED tester:
```
Create Led Tester               sysbus.gpio.led
```
Then, execute one of the following commands:
* Check if the GPIO pin matches the expected state at some point during the entire `<timeout>` period. If `<timeout>` equals 0, the check is performed immediately and fails if the pin state is incorrect.
  ```
  Assert Led State                <False/True>  timeout=<timeout>
  ```
* Check if the GPIO pin matches the expected state during `<timeout>`, and if the states lasted for a given period.
  ```
  Assert And Hold LED State  true  timeoutAssert=0.1  timeoutHold=2
  ```
* Check if a LED is blinking in a pattern determined by given parameters.
  ```
  Assert Led Is Blinking    testDuration=0.05  onDuration=0.005  offDuration=0.005  tolerance=0.2
  ```

To set a GPIO input through a button, use one of the following options:
* Use the `Press` and `Release` button commands to set the GPIO pin to 1 and 0, respectively. Alternatively, you can use the `Toggle` command to change the current state to an opposite one.
  ```
  Execute Command          gpio.button Press
  Execute Command          gpio.button Release
  Execute Command          gpio.button Toggle
  ```
* Use the `PressAndRelease` button command to change the button state to 1 and then immediately to 0.
  ```
  Execute Command          gpio.button PressAndRelease
  ```

For more details, see the [Led Tester Keywords implementation](https://github.com/renode/renode/blob/master/src/Renode/RobotFrameworkEngine/LedKeywords.cs), [Button implementation](https://github.com/renode/renode-infrastructure/blob/master/src/Emulator/Peripherals/Peripherals/Miscellaneous/Button.cs) and the [example test case](https://github.com/renode/renode/blob/master/tests/platforms/NRF52840.robot#L104).

  
## Network interfaces
To test a network interface (either a radio or Ethernet), first create a network tester:
```
Create Network Interface Tester                sysbus.ethernet
```
Then, you can verify network traffic withthe command below. Here, the parameters are responsible for an expected bytes pattern (with the `_` wildcard), for an index of the first byte in a packet that needs to be checked, and for the number of packets that need to be checked before failing.
```
Wait For Outgoing Packet With Bytes At Index    0800__________________11____C0000201E0000181013F013F________0012  12  5  10
```


Use the command below to run a simulation until a packet is received or a timeout is triggered:
```
Wait For Outgoing Packet <timeout> 
```

To send a packet to an interface, use the following command:
```
Send Frame    <bytes>
```
For more details, see the [Network Interface Keywords implementation](https://github.com/renode/renode/blob/master/src/Renode/RobotFrameworkEngine/NetworkInterfaceKeywords.cs) and the [example testcase](https://github.com/renode/renode/blob/master/tests/platforms/nucleo_h753zi.robot#L276).

## Verifying other interfaces

To test communication through the I2C or SPI without a target device, we use dummy target devices with some enqueued data to respond with.

A verification is typically based on software behavior, e.g. matching a line on a UART.

For more complex scenarios, you can create an ad-hoc compiled I2C or SPI target device with verification implemented in C#.

### I2C

First, create a `DummyI2CSlave`:
```
Execute Command          machine LoadPlatformDescriptionFromString "dummy_i2c: Mocks.DummyI2CSlave @ lpi2c0 42"
```

The `DummyI2CSlave` peripheral is designed to be interfaced via commands but can also be scripted through IronPython integration.

You can find an example of a Python-scripted I2C target device in [echo-i2c-peripheral.py](https://github.com/renode/renode/blob/master/tests/platforms/echo-i2c-peripheral.py).

More information on the Python-enabling features is available in the [Dummy I2C Slave](https://renode.readthedocs.io/en/latest/basic/using-python.html#dummy-i2c-slave) section of Renode documentation.

You can queue response data with the following command:

```
Execute Command          dummy_si2c EnqueueResponseByte 0x2a
```
See the [example test case](https://github.com/renode/renode/blob/master/tests/platforms/Renesas_RA8M1.robot#L147) for usage.
### SPI

First, create a `DummySPISlave`:
```
Execute Command          machine LoadPlatformDescriptionFromString "dummy_spi: Mocks.DummySPISlave @ lpspi0 42"
```

The dummy SPI supports only queuing response data. To do so use the following command:

```
Execute Command          dummy_spi EnqueueValue 0x2a
```

In addition to the verification based on software behavior, you can check the data sent against a log entry:

```
Wait For Log Entry       dummy_spi: Data received: 0xA
```
See the [example test case](https://github.com/renode/renode/blob/master/tests/platforms/ambiq-apollo4.robot#L131) for usage.

