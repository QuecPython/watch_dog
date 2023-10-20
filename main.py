
from usr.watch_dog import WDG
from queue import Queue
from machine import WDT
import _thread
import utime

print("================== Watch dog tests ==================")

# Initialize the hardware watchdog.
print("[%s] Initialize the hardware watchdog." % __name__)
print("[%s] The hardware watchdog must be fed with a period less than 20 seconds." % __name__)
wdt = WDT(30)

# The behavior function that triggers the watchdog 
# suggests adding a hardware watchdog here to ensure the security of the software watchdog thread
def feed_lower(args):
    print("[%s] Feed the hardware watchdog exactly." % __name__)
    wdt.feed()

# Initialize the software watchdog.
print("[%s] Initialize the software watchdog." % __name__)
print("[%s] Feed the hardware watchdog every 10 seconds." % __name__)
WDG.init(10, feed_lower)

# Create a queue for the communication between app_thread_1 and app_thread_2.
print("[%s] Create a queue for the communication between app_thread_1 and app_thread_2." % __name__)
queue = Queue()

# app_thread_1
def app_thread_1():
    print("[%s] Thread started." % "app_thread_1")
    print("[%s] Create a software watchdog." % "app_thread_1")
    print("[%s] We pretend that the thread will block for up to 5 seconds during normal operation." % "app_thread_1")
    wdg = WDG.create(5)

    for i in range(10):
        print("[%s] Feed the watchdog." % "app_thread_1")
        wdg.feed()

        print("[%s] Send a message to queue: %s." % ("app_thread_1", "A message from app_thread_1"))
        queue.put("A message from app_thread_1")

        if i < 9:
            print("[%s] Will feed the watchdog again after sleeping for 5 seconds." % "app_thread_1")
            utime.sleep(5)
        else:
            print("[%s] Sleep for a long time to simulate a scenario" % "app_thread_1")
            print("    where an abnormality occurs and the dog cannot be fed in time.")
            utime.sleep(1800)

# app_thread_2
def app_thread_2():
    print("[%s] Thread started." % "app_thread_2")
    print("[%s] Create a software watchdog." % "app_thread_2")
    print("[%s] We pretend that the thread will block for up to 15 seconds during normal operation." % "app_thread_2")
    wdg =  WDG.create(15, queue)

    while True:
        print("[%s] Feed the watchdog." % "app_thread_2")
        wdg.feed()

        print("[%s] Waiting for a message from queue." % "app_thread_2")
        print("[%s] Will feed the watchdog again after getting the message." % "app_thread_2")

        msg = queue.get()
        if msg:
            print("[%s] Got the message: %s." % ("app_thread_2", msg))
        else:
            print("[%s] Got a None message from the underlying watchdog mechanism." % "app_thread_2")


# Start Child thread test 1
print("[%s] Create a thread named <app_thread_1>." % __name__)
_thread.start_new_thread(app_thread_1, ())

# Start Child thread test 2
print("[%s] Create a thread named <app_thread_2>." % __name__)
_thread.start_new_thread(app_thread_2, ())
