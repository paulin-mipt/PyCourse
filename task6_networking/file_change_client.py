'''
Created on May 8, 2014
@author: paulin
'''

import socket, argparse, os

HOST, PORT = "localhost", 9941

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
parser = argparse.ArgumentParser(description='SuperDocumentReverser')
parser.add_argument('paths', metavar = 'path', type = str, nargs = 1, 
                    help = 'path of a text file to reverse')
args = parser.parse_args()
filepath = args.paths[0]
if not os.path.exists(filepath):
    print("{} : no such path".format(filepath))
    exit()

try:
    sock.connect((HOST, PORT))
    with open(filepath) as fread:
        for line in fread:
            if line[-1] == "\n":
                line = line[:-1]
            sock.sendall(bytes("s" + line + "eol\n", "utf-8"))
    sock.sendall(bytes("eof\n", "utf-8"))
    
    received = sock.recv(2048).decode("utf-8")
    fwrite = open(filepath, 'w')
    while len(received) > 0:
        fwrite.write(received)
        received = sock.recv(2048).decode("utf-8")
    fwrite.close()
finally:
    sock.close()
