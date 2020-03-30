# ezasyncio
Simplified multithreading in python
Example code:

```python
	import time
	def foo(arg1, arg2):
	    time.sleep(5)
	    print("foo exiting, arg1: %s, arg2: %s" % (arg1, arg2))
	a = asyncez(foo, "hello", "world")
	a.run()
	print("foo is running now :)")
	time.sleep(6)
	print("Main is exiting")
```

Expected output:

```
  4:21:00 >> foo is running now :)
  4:21:05 >> foo exiting, arg1: hello, arg2: world
  4:21:06 >> main is exiting
```
