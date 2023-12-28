# Debugging software with Visual Studio Code

Debugging software on machines emulated in Renode using GDB is also available for VS Code users.

## Renode script 

```cpp
# Most of Renode scripts use the bin variable to specify an executable to run.
$bin ?= $CWD/zephyr/build/zephyr/zephyr.elf
include @scripts/single-node/stm32l072.resc

# It's required to start a GDB server in Renode.
machine StartGdbServer 3333
```

## Tasks

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Build application", // Feel free to create your own build task.
            "type": "shell",
            "command": "west",
            "args": [
                "build",
                "--pristine=auto",
                "--build-dir",
                "zephyr/build",
                "--board",
                "b_l072z_lrwan1",
                "zephyr/samples/subsys/shell/shell_module"
            ],
            "problemMatcher": [
                "$gcc"
            ],
            "group": "build",
            "presentation": {
                "reveal": "silent"
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
            "group": "none",
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            }
        }
    ]
}
```

## Launch

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug application in Renode",
            "type": "cppdbg",
            "request": "launch",
            "preLaunchTask": "Run Renode",
            "miDebuggerServerAddress": "localhost:3333",
            "cwd": "${workspaceRoot}",
            "miDebuggerPath": "gdb-multiarch", // Use an architecture-specific version of GDB instead.
            "program": "${workspaceRoot}/zephyr/build/zephyr/zephyr.elf" // Binary to debug
        }
    ]
}
```