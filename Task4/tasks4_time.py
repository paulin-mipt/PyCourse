import time

def time_counter(fn):
    def wrapped(*args):
        t1 = time.time()
        fn(*args)
        t2 = time.time()
        print(t2 - t1)
    return wrapped