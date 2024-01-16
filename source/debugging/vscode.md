# Debugging software with Visual Studio Code

Debugging software on machines emulated in Renode using GDB is also available for VS Code users.

In order to enable single-click debugging in Renode, you need to configure VS Code appropriately.

Renode can run any software, but for the sake of this chapter, we will use a sample configuration for running a TFLite Micro demo on Zephyr RTOS built for the nRF52840 board.

Such a configuration consists of 4 files:
* .vscode/launch.json
* .vscode/tasks.json
* platform.resc
* debug.conf

The sample configuration files are located in the `/tools/vscode_config/` directory in the Renode repository.

All of these files include inline comments with additional explanations.

```{note}
Please note that JSON format does not support comments, but VSCode handles them without issue.
```

For the provided config files, the VSCode workspace root directory is the directory where "west init" was run, i.e. the directory that contains Zephyr, modules, tools, etc. - all paths are relative to that location.

Place the configuration files in the workspace root directory or adjust the paths in the scripts accordingly.

```{note}
The .vscode directory might be hidden in some file explorers.
```

## Launch configuration

The "launch.json" file describes a launch configuration named "Debug application in Renode". 
If needed, adjust the path to the ELF file and the GDB version to be used for debugging. 

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug application in Renode",
            "type": "cppdbg",
            "request": "launch",
            "preLaunchTask": "Run Renode",
            "postDebugTask": "Close Renode",
            "miDebuggerServerAddress": "localhost:3333",
            "cwd": "${workspaceRoot}",
            "miDebuggerPath": "arm-zephyr-eabi-gdb",
            "program": "${workspaceRoot}/build/zephyr/zephyr.elf"
        }
    ]
}
```

## Defining tasks

The sample `tasks.json` file defines three tasks:

1. "Build application" is a sample build task for this particular scenario. 
Please adjust to your needs. Mind that the generated binary (needs to be an ELF file for effective debugging) is referenced in "platform.resc" and "launch.json".

1. "Run Renode" runs after "Build application" finishes. 
It starts the "platform.resc" script and waits for the GDB server to start. 
It requires a proper path to the resc script.

1. "Close Renode" is a task fired when you close the debugging session. It will shut down Renode, and it's a matter of personal preference if you want to use it or not. You can disable it in "launch.json" by removing/commenting-out the "postDebugTask" line.

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Build application",
            "type": "shell",
            "command": "west",
            "args": [
                "build",
                "--pristine",
                "--board",
                "nrf52840dk_nrf52840",
                "zephyr/samples/modules/tflite-micro/hello_world",
                "--",
                "-DEXTRA_CONF_FILE=${workspaceFolder}/debug.conf"
            ],
            "problemMatcher": [
                "$gcc"
            ],
            "group": "build",
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            }
        },
        {
            "label": "Run Renode",
            "type": "shell",
            "command": "renode",
            "args": [
                "${workspaceFolder}/platform.resc"
            ],
            "dependsOn": [
                "Build application"
            ],
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
            "group": "build",
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            }
        },
        {
            "label": "Close Renode",
            "command": "echo ${input:terminate}",
            "type": "shell",
            "problemMatcher": []
        }
    ],
    "inputs": [
        {
            "id": "terminate",
            "type": "command",
            "command": "workbench.action.tasks.terminate",
            "args": "terminateAll"
        }
    ]
}
```

## Renode simulation script 

The "platform.resc" file is a sample Renode simulation script:

```
$bin ?= $CWD/build/zephyr/zephyr.elf
include @scripts/single-node/nrf52840.resc

machine StartGdbServer 3333
```

It contains two important parts: 
- specifying the ELF file 
- starting GDB as the last command in the script. 
You will need to adjust the file to your particular needs.

You can use this script to setup the entire simulation or rely on a predefined script.
Most of Renode scripts use the `bin` variable to specify an executable to run.
It should also match the configuration in `launch.json`.

## debug.conf

The "debug.conf" file is Zephyr-specific. 
It is used to disable optimizations during compilation, as certain optimizations may hinder the debugging process. 
You can remove this file altogether, depending on the way you select optimizations.
