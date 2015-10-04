import http.server
import socketserver


class LjonHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = './public/{}'.format(self.path)
        super().do_GET()


class Server(object):
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port

    def start(self):
        httpd = socketserver.TCPServer((self.host, self.port),
                                       LjonHTTPRequestHandler)

        print('Running HTTP server on {host}:{port}'.format(host=self.host,
                                                            port=self.port))
        httpd.serve_forever()
