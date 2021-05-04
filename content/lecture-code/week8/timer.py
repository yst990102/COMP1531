import threading
import time
 
def hello():
    print("hello, Timer")
    # do something
 
if __name__ == '__main__':
    t = threading.Timer(3.0, hello)
    t.start()
    print("Starting")