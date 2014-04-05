def remove_prefix(s):
    return s[s.find('-') + 1:]
    
def reverse_list(l):
    l.reverse()
    return l

def different(a, b, c):
    return len({a, b, c}) == 3

def sort_dict(d):
    for key in sorted(d.keys()):
        print(key + ':' + d[key])

import functools
def fact(n):
    return functools.reduce(lambda a, b : a * b, range(1, n))
#print(fact(2000))

def table():
    a = [[i*j for j in range(1,10)] for i in range(1,10)]
    for i in range(9):
        print(" ".join([format(a[i][j], "2g") for j in range(9)]))

table()


def fib(n):
    a = 1
    b = 1
    k = 0
    while not (a == 0 and b == 1):
        c = a + b
        a = b
        b = c            
        print(c % 10)
        k += 1
    print(k)