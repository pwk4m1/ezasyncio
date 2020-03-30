#!/usr/local/bin/python3
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


