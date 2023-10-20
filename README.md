# QuecPython soft watch dog

[[中文](README_ZH.md)]

QuecPython The software watchdog solution can solve the running safety problem of the QuecPython subthread, which is convenient to restart the application or restart the system when the APP application fails to execute abnormally.

## init soft watch dog

### `WDG.init`

```python
# import lib
from usr.watch_dog import WDG
# Initialize the software watchdog parameters
WDG.init(feed_cycle, feed_impl=None, *args)
```

The software watchdog parameters are initialized by the software watchdog object.

**Parameter description:**

- `feed_cycle` - The period of the software watchdog, that is, how often to check the running status of child threads, is shorter than that of the hardware watchdog
- `feed_impl` - The feeding function of the software watchdog is to trigger the actions of the watchdog after feeding the dog, such as restarting, etc. It is recommended to add the feeding action of the hardware watchdog to the function
- `args` - The parameter you want to pass to the implementation function

## create watch dog object

### `WDG.create`

```python
# Bind the watchdog to the corresponding subthread
wdg = WDG.create(timeout, queue=None)
```

Call this method in the child thread that needs to join the watchdog, before the child thread loops.

**Parameter description:**

- `timeout`- Cycle period of the child thread, unit: second. For example, the child thread cycles once every second. The parameter is passed as 1
- `queue`- Queue of child threads. If the child thread is implemented through a queue, this queue is passed to the child thread queue. If there is no queue, there is no need to pass it

## feed watch dog

### `wdg.feed`

```python
# feed watch dog in child thread
wdg.feed()
```

This method is called in the child thread that needs to be added to the watchdog, once per loop.

## delete watch dog object

### `wdg.destroy`

```python
# The child thread is unbound from the watchdog. Procedure
wdg.destroy()
```

Call this method in the child thread that needs to be added to the watchdog to unbind the watchdog object to that thread

