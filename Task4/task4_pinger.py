import threading
import subprocess
import argparse

def ping_host(host, num):  
    PIPE = subprocess.PIPE
    p = subprocess.Popen(" ".join(["ping", host]), shell=True, stdin=PIPE, stdout=PIPE,
        stderr=subprocess.STDOUT, close_fds=True)
    answer = " "
    while answer:
        answer = p.stdout.readline()
        print('thread', num, 'received answer', answer[:-1])

parser = argparse.ArgumentParser(description='Pinger v.0.0.9')
parser.add_argument('hosts', metavar = 'host', type = str, nargs = '+', 
                    help = 'IP addresses, such as 127.0.0.1')
args = parser.parse_args()
threads = []
for i in range(len(args.hosts)):
    t = threading.Thread(target=ping_host, args=(args.hosts[i],i,))
    threads.append(t)
    t.start()