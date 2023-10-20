# QuecPython 软件看门狗

[[English](README.md)]

QuecPython 软件看门狗方案可以解决QuecPython子线程运行安全问题，方便在APP应用程序发生异常不执行时进行重启应用或者重启系统等操作。

## 初始化软狗

### `WDG.init`

```python
# 导入库
from usr.watch_dog import WDG
# 初始化软件看门狗参数
WDG.init(feed_cycle, feed_impl=None, *args)
```

通过软件看门狗对象初始化软件看门狗参数。

**参数描述：**

- `feed_cycle` - 软件看门狗的周期，即为多久检查一次子线程的运行情况，建议设置的比硬件看门狗的周期短
- `feed_impl` - 软件看门狗的喂狗实现函数，即为触发看门狗喂狗之后的动作，例如重启等，建议在函数中添加硬件看门狗的喂狗动作
- `args` - 想要传给实现函数的参数

## 创建软狗对象

### `WDG.create`

```python
# 绑定看门狗到对应子线程
wdg = WDG.create(timeout, queue=None)
```

在需要加入看门狗的子线程中调用此方法,注意需要在子线程循环之前。

**参数描述：**

- `timeout`- 子线程的循环周期，单位：秒，例如子线程一秒循环一次，参数传1
- `queue`- 子线程队列，如果子线程是通过队列实现的，该处传子线程队列，如果没有就不用传

## 喂狗

### `wdg.feed`

```python
# 子线程喂狗
wdg.feed()
```

在需要加入看门狗的子线程中调用此方法，子线程每循环一次调用一次。

## 删除软狗对象

### `wdg.destroy`

```python
# 子线程解除绑定看门狗
wdg.destroy()
```

在需要加入看门狗的子线程中调用此方法，解除该线程绑定的看门狗对象

