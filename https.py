import http.server
import ssl


httpd = http.server.HTTPServer(('10.243.106.192', 8000), http.server.SimpleHTTPRequestHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Serving on https://10.243.106.192:8000")
httpd.serve_forever()

