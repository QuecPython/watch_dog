# QuecPython Watchdog Component API Reference Manual

The QuecPython watchdog component is designed to provide a separate software watchdog object for each thread. Users can call the `WDG.create` method in a thread to create a software watchdog object `wdg` and call the `wdg.feed` method to feed the watchdog.

This watchdog component essentially implements a voting mechanism. Threads that have created a software watchdog need to periodically call the `wdg.feed` method to feed the watchdog. This feeding action is equivalent to voting. When all threads that have created a software watchdog object have fed the watchdog, the hardware watchdog will be triggered to feed.

## Initialize Watchdog Component

### `WDG.init`

```python
WDG.init(feed_cycle, feed_impl=None, *args)
```

**Parameters**

- `feed_cycle` - The feeding cycle of the hardware watchdog.
- `feed_impl` - The feeding method of the hardware watchdog.
    - The watchdog component determines whether the hardware watchdog needs to be fed based on the voting feeding situation of application threads, with `feed_cycle` as the cycle.
    - The prototype is `feed_impl(args)`. The `args` parameter passed to the `WDG.init` method will be passed to the `feed_impl` method for users to pass custom parameters.
- `args` - Parameters passed to the `feed_impl` method.

> Call this method before creating any software watchdog objects. It is generally called during application initialization.

## Create Software Watchdog Object

### `WDG.create`

```python
wdg = WDG.create(timeout, queue=None)
```

**Parameters**

- `timeout` - The feeding cycle of the software watchdog, in seconds.
- `queue` - Message queue.
    - When an application thread that needs to feed the watchdog has a scenario of waiting permanently for messages in the message queue, to avoid the thread being unable to continue running due to the message queue having no messages for a long time and thus unable to feed the watchdog, the message queue can be passed to the watchdog component when creating the software watchdog. The watchdog component will send empty messages to the queue at `feed_cycle` intervals to trigger the application thread to continue running and get a chance to feed the watchdog.

**Return Value**

Returns the software watchdog object `wdg`.

> - This method is called within the application thread that needs to feed the watchdog, generally before the while loop.
> - If a message queue is added when creating the software watchdog object, the application thread needs to check if the messages are empty when processing messages.

## Feed Software Watchdog

### `wdg.feed`

```python
wdg.feed()
```

> - This method is called by the application thread, generally within the while loop.
> - If the software watchdog is not fed within the feeding cycle, the hardware watchdog will not be fed.

## Delete Software Watchdog

### `wdg.destroy`

```python
wdg.destroy()
```

> - This method is called within the application thread that has already created a software watchdog object.
> - Once the software watchdog object is deleted, the application thread will no longer feed the watchdog, and the watchdog component will no longer consider this application thread in the voting mechanism.
> - Generally, there is no need to delete the software watchdog object.