'''
Created on May 8, 2014
@author: paulin
'''
import socketserver, threading

class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        count = 0
        lines = []
        lines.append(self.rfile.readline().decode("utf-8")[:-3])
        while len(lines[count]) > 0:
            print("asked", lines[count])
            count += 1
            lines.append(self.rfile.readline().decode("utf-8")[:-3])
        for i in range(len(lines) - 1):
            self.wfile.write(bytes(lines[i][::-1], "utf-8"))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    PORT = 9949
    server = ThreadedTCPServer(("localhost", PORT), MyTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    server_thread.join()