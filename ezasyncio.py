#!/usr/local/bin/python3
"""
BSD 3-Clause License

Copyright (c) 2020, k4m1
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import threading
import asyncio

# This class aims to ease up managing multithreaded programs in python.
# I found it out as annoying task to do/implement each time, so here we go
#
# This class takes fairly simple arguments.
#   fun: function to execute
#   args: arguments to provide for fun
#   timeout: .. timeout for fun() to finish.
#
# Return value of provided function can be accessed via asyncez.return_value.
#
# Example code:
# --------------------------------------------------------------------------
# import time
# def foo(arg1, arg2):
#     time.sleep(5)
#     print("foo exiting, arg1: %s, arg2: %s" % (arg1, arg2))
#
# a = asyncez(foo, "hello", "world")
# a.run()
# print("foo is running now :)")
# time.sleep(6)
# print("Main is exiting")
# --------------------------------------------------------------------------
# Expected output:
#   4:21:00 >> foo is running now :)
#   4:21:05 >> foo exiting, arg1: hello, arg2: world
#   4:21:06 >> main is exiting
#
class asyncez:
    def __init__(self, fun, *args, async_timeout=None):
        self.fun            = fun
        self.args           = args
        self.timeout        = async_timeout
        self.return_value   = None
        self.task           = None 

    # Execute user-provided function
    async def __exec(self):
        self.return_value = self.fun(*self.args)

    # Stop executing user-provided function immediately, kill the thread.
    def stop(self):
        self.task.cancel()

    async def __start_async(self):
        self.task = asyncio.create_task(self.__exec())
        try:
            if (self.timeout == None):
                await self.task
            else:
                await asyncio.wait_for(self.task, timeout=self.timeout)
        except asyncio.TimeoutError:
            pass
    
    def async_wrapper(self):
        asyncio.run(self.__start_async())

    def run(self):
        threading.Thread(target=self.async_wrapper).start()


