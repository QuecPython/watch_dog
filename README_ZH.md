# QuecPython 软件看门狗

中文 | [English](README.md)

## 概述

QuecPython 看门狗组件在设计上为每一个线程提供单独的软件看门狗对象，用户可以在线程中调用 `WDG.create` 方法创建一个软件看门狗对象 `wdg`，并调用 `wdg.feed` 方法喂狗。

该看门狗组件本质上是基于投票机制来实现的。创建了软件看门狗的线程需周期性调用 `wdg.feed` 方法喂狗，该喂狗动作即为投票。当所有创建了软件看门狗对象的线程均喂狗了，硬件上的看门狗会被触发喂狗。

## 用法

- [API 参考手册](./docs/zh/API参考手册.md)
- [示例代码](./code/demo.py)

## 贡献

我们欢迎对本项目的改进做出贡献！请按照以下步骤进行贡献：

1. Fork 此仓库。
2. 创建一个新分支（`git checkout -b feature/your-feature`）。
3. 提交您的更改（`git commit -m 'Add your feature'`）。
4. 推送到分支（`git push origin feature/your-feature`）。
5. 打开一个 Pull Request。

## 许可证

本项目使用 Apache 许可证。详细信息请参阅 [LICENSE](LICENSE) 文件。

## 支持

如果您有任何问题或需要支持，请参阅 [QuecPython 文档](https://python.quectel.com/doc) 或在本仓库中打开一个 issue。
