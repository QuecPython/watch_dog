# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
#  
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  
#     http://www.apache.org/licenses/LICENSE-2.0
#  
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import _thread
import utime
import sys

class __WatchDog(object):
    def __init__(self, wdg):
        self.__wdg = wdg

    def feed(self):
        self.__wdg.__feed()

    def destroy(self):
        self.__wdg.__destroy()

class _WatchDog(object):

    def __init__(self):
        self.__feed_cycle = None
        self.__feed_impl = None
        self.__feed_impl_args = None
        self.__tid = None
        self.__lock = None
        self.__thread_dict = None

    def __destroy(self):
        with self.__lock:
            if _thread.get_ident() in self.__thread_dict:
                del self.__thread_dict[_thread.get_ident()]

    def __feed(self):
        with self.__lock:
            tid = _thread.get_ident()
            if tid in self.__thread_dict:
                self.__thread_dict[tid]['flag'] = True

    def __feed_task(self):
        while True:
            with self.__lock:
                should_feed = True
                for tid, data in self.__thread_dict.items():
                    if data['flag'] is False:
                        timeout = data['timeout']
                        if timeout != -1:
                            last_feed_time = data['last_feed_time']
                            interval = utime.time() - last_feed_time
                            if interval > timeout:
                                should_feed = False
                                break

            if should_feed:
                with self.__lock:
                    if callable(self.__feed_impl):
                        self.__feed_impl(self.__feed_impl_args)
                    for tid, data in self.__thread_dict.items():
                        if data['flag'] is True:
                            data['last_feed_time'] = utime.time()
                            data['flag'] = False

            utime.sleep(self.__feed_cycle)

            with self.__lock:
                for tid, data in self.__thread_dict.items():
                    if data['queue']:
                        data['queue'].put(None)

    def __start(self, *args):
        if not self.__tid or (self.__tid and not _thread.threadIsRunning(self.__tid)):
            try:
                _thread.stack_size(0x1000)
                self.__tid = _thread.start_new_thread(self.__feed_task, ())
            except Exception as e:
                sys.print_exception(e)

    def __stop(self, *args):
        if self.__tid:
            try:
                _thread.stop_thread(self.__tid)
            except:
                pass
        self.__tid = None

    def init(self, feed_cycle, feed_impl = None, *args):
        self.__feed_cycle = feed_cycle
        self.__feed_impl = feed_impl
        self.__feed_impl_args = args
        self.__tid = None
        self.__lock = _thread.allocate_lock()
        self.__thread_dict = {}
        self.__start()

    def deinit(self):
        self.__stop()

    def create(self, timeout, queue = None):
        with self.__lock:
            if _thread.get_ident() not in self.__thread_dict:
                self.__thread_dict[_thread.get_ident()] = {
                    'timeout': timeout,
                    'flag': True,
                    'last_feed_time': utime.time(),
                    'queue': queue
                }

        return __WatchDog(self)

WDG = _WatchDog()
