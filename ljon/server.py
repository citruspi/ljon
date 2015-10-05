import http.server
import socketserver
import os


class Server(object):
    def __init__(self, host, port, context):
        self.host = host
        self.port = port
        self.context = context

    def start(self):
        os.chdir(self.context.public_path)
        httpd = socketserver.TCPServer((self.host, self.port),
                                       http.server.SimpleHTTPRequestHandler)

        print('Running HTTP server on {host}:{port}'.format(host=self.host,
                                                            port=self.port))
        httpd.serve_forever()
