# Debugging software with Visual Studio Code

Debugging software on machines emulated in Renode using GDB is also available for VS Code users.

## Renode script 

```cpp
:name: Ambiq Apollo 4
:description: This script runs the Ambiq Suite's Hello World Uart example on Ambiq Apollo 4.

using sysbus
$name?="Ambiq Apollo 4"
mach create $name

machine LoadPlatformDescription @platforms/cpus/ambiq-apollo4.repl #adjust
showAnalyzer uart2

$bin?=@build/zephyr/zephyr.elf #adjust
macro reset
"""
    sysbus LoadELF $bin
"""

runMacro $reset

cpu StartGdbServer 3333

sleep 3
```

## Tasks

```json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Renode",
            "type": "shell",
            "command": "./renode",
            "args": [
                "-e",
                "set bin @/home/codespace/zephyrproject/zephyr/build/zephyr/zephyr.elf;i @scripts/single-node/stm32l072.resc;machine StartGdbServer 3333 True"], // adjust
            "options": {
                "cwd": "/home/codespace/renode" // adjust
            },
            "isBackground": true,
            "problemMatcher": {
                "source": "Renode",
                "pattern": {
                    "regexp": ""
                },
                "background": {
                    "activeOnStart": true,
                    "beginsPattern": "Renode, version .*",
                    "endsPattern": ".*GDB server with all CPUs started on port.*"
                }
            },
            "group": "none",
            "presentation": {
                "reveal": "silent",
                "panel": "shared"
            }
        },
        {
            "label": "Build application",
            "type": "shell",
            "command": "west build --pristine -b b_l072z_lrwan1 samples/subsys/shell/shell_module", // adjust
            "options": {
                "cwd": "/home/codespace/zephyrproject/zephyr" // adjust
            },
            "problemMatcher": []
        },
        {
            "label": "Build application and run Renode",
            "dependsOrder": "sequence",
            "dependsOn": ["Build application", "Run Renode"],
            "problemMatcher": []
        }
    ]
}
```

## Launch

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "cwd": "${workspaceRoot:zephyr}", // adjust
            "executable": "build/zephyr/zephyr.elf", // adjust
            "type": "gdb",
            "request": "attach",
            "name": "Debug application in Renode",
            "preLaunchTask": "Build application and run Renode",
            "target": ":3333",
            "gdbpath": "gdb-multiarch", // adjust
            "remote": true,
        }
    ]
}
```