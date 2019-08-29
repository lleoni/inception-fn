#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import time
import json
from urllib.parse import urlparse, parse_qs

hostName = ''
hostPort = 80

import sys
import inception


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        self._set_headers()
        imageUrl = query_components.get('imageUrl')
        if imageUrl is None:
            self.wfile.write(json.dumps([{'error':'imageUrl parameter required'}]).encode('utf-8'))  
            return
        imageUrl = imageUrl[0]
        print('imageUrl to download --> %s' % (imageUrl))
        try:
            result = inception.invoke(imageUrl)
            self.wfile.write(result.encode('utf-8'))
        except Exception as err:
            print("Error {}".format(err)) 
            self.wfile.write(json.dumps([{'error': str(err) }]).encode('utf-8'))

myServer = HTTPServer((hostName, hostPort), SimpleHTTPRequestHandler)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))

