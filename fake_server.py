import http.server
import ssl

PORT = 443


class FakeHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"I am a fake web page")


handler = FakeHandler

httpd = http.server.HTTPServer(("0.0.0.0", PORT), handler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    certfile="/etc/ssl/certs/server.crt", keyfile="/etc/ssl/private/server.key"
)

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)


print(f"Serving HTTPS on port {PORT}")
httpd.serve_forever()
