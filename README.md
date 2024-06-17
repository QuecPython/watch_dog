# QuecPython Software Watchdog

[中文](README_ZH.md) | English

## Overview

The QuecPython watchdog component is designed to provide a separate software watchdog object for each thread. Users can call the `WDG.create` method in a thread to create a software watchdog object `wdg` and call the `wdg.feed` method to feed the watchdog.

This watchdog component essentially implements a voting mechanism. Threads that have created a software watchdog need to periodically call the `wdg.feed` method to feed the watchdog. This feeding action is equivalent to voting. When all threads that have created a software watchdog object have fed the watchdog, the hardware watchdog will be triggered to feed.

## Usage

- [API Reference Manual](./docs/en/API_Reference.md)
- [Example Code](./code/demo.py)

## Contribution

We welcome contributions to improve this project! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for details.

## Support

If you have any questions or need support, please refer to the [QuecPython documentation](https://python.quectel.com/doc/en) or open an issue in this repository.