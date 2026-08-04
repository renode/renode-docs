# Virtual Time Scheduling Mechanisms

Renode provides several mechanisms for scheduling actions. Although these mechanisms may appear similar, each of them provides different execution and synchronization guarantees.

## Scheduled Actions

Scheduled actions are strongly related to *Time Framework* and allow registering some one-shot callbacks in specific points of the machine's virtual time.

They may be useful for operations such as:
- delaying peripheral operation
- changing a device state after a defined delay
- generating some event without creating a dedicated timer

A scheduled action is executed when the machine's virtual time reaches the requested timestamp. The whole operation should be short and non-blocking. The callback is executed on a CPU thread responsible for virtual time progression. A machine's virtual time is the minimum value reported by all of its CPUs.

**IMPORTANT:** Scheduling action during an already executing grant may use unsynchronized virtual time and introduce some timing inaccuracies.

Example:
```c#
machine.ScheduleAction(
    TimeInterval.FromMicroseconds(10),
    (elapedVirtualTime) => Logger.Log(LogLevel.Info, "Elapsed virtual time after 10us: {0}", elapedVirtualTime),
    "Simple scheduled action"
);
```

**IMPORTANT:** During the execution of this callback, the remaining CPUs may still be running.

## Synced State

Last phase of *time source* execution (sync phase). During it, all statements below are true:
- all time sinks have completed their grants
- no CPU registered in this time source should still be executing

This mechanism is a good choice for operations that require a stable emulation state, such as resetting, applying some global changes or just preventing race conditions among CPUs.

Currently, there are two variants of this operation:
- `ExecuteInNearestSyncedState` - queues a callback for the nearest synchronized state. If `executeImmediately` is set to true and the method is called from the thread currently executing the synchronization phase, the callback is executed immediately. Otherwise it will execute in next one.
- `ExecuteInSyncedState` - queues a callback for the nearest synchronized state at or **after** the specified timestamp.

Example:
```c#
machine.LocalTimeSource.ExecuteInNearestSyncedState(
    (stamp) => Logger.Log(LogLevel.Info, "All CPUs are now waiting, each of them executed exactly {0}", stamp.TimeElapsed)
);


machine.LocalTimeSource.ExecuteInSyncedState(
    (stamp) => Logger.Log(LogLevel.Info, "All CPUs are now waiting, but this action happened at {0}", stamp.TimeElapsed),
    TimeDomainsManager.Instance.VirtualTimeStamp
);
```

**NOTE**: If you have a machine object and want to simply register some event, without touching *time source* directly, there is some really useful method called `HandleTimeDomainEvent`. Here's an usage example
```c#
var currentTimeStamp = TimeDomainsManager.Instance.VirtualTimeStamp;

machine.HandleTimeDomainEvent<TimeStamp>(
    (stamp) => Logger.Log(LogLevel.Info, "This event was registered directly in machine at {0}", stamp.TimeElapsed),
    currentTimeStamp,
    currentTimeStamp,
    () => Logger.Log(LogLevel.Info, "This callback is called after the first one. However it is optional")
);
```

## Managed Threads

`IManagedThread` represents a periodic action driven by the machine's virtual time.

Despite its name, it does not create a dedicated `Thread`, but instead uses a mechanism similar to *Scheduled Actions*.

A managed thread can be:
- started
- stopped
- restarted
- started with some virtual time delay
- configured with a specific frequency

Managed threads are designed for short, periodic operations such as sensor sampling, queue processing or simple peripheral updates. Their callbacks cannot block, sleep or contain infinite loops, because they are executed synchronously by CPU thread responsible for virtual time progression.

Example:
```c#
machine.ObtainManagedThread(
    () => Logger.Log(LogLevel.Info, "This callback will be executed 1000 times in 1 virtual second"),
    1000,
    "Some managed thread"
);

machine.ObtainManagedThread(
    () => Logger.Log(LogLevel.Info, "This callback will be executed every 10ms of virtual time"),
    TimeInterval.FromMilliseconds(10),
    "Another managed thread"
);
```

**IMPORTANT:** During the execution of this callbacks, the remaining CPUs may still be running.