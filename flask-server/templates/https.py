import http.server
import ssl


httpd = http.server.HTTPServer(('10.5.12.118', 8000), http.server.SimpleHTTPRequestHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
#context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

print("Serving on https://10.5.12.118:8000")
httpd.serve_forever()