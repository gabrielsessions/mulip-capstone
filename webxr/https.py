import http.server
import ssl

IP = "localhost"

httpd = http.server.HTTPServer((IP, 8000), http.server.SimpleHTTPRequestHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Serving on https://" + IP)
httpd.serve_forever()

