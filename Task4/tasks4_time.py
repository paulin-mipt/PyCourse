import time

def time_counter(fn):
    def wrapped(*args, **kwargs):
        t1 = time.monotonic()
        res = fn(*args, **kwargs)
        t2 = time.monotonic()
        print("time of processing in seconds:", t2 - t1)
        return res
    return wrapped

@time_counter
def summ(a, b, c):
    return a + b + c

print(summ(1, 2, 3))