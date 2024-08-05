#!/usr/bin/python
from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qsl, urlparse
import response
from datatypes import htmldoc

class headers:
  def __init__(self, headers):
    self.headers = headers
  def items(self):
    return self.headers

class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
      return urlparse(self.path)

    @cached_property
    def query_data(self):
      return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
      content_length = int(self.headers.get("Content-Length", 0))
      return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
      return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
      return SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self):
      data = response.respond(self)
      self.send_response(data.status)
      for header in data.headers:
        self.send_header(header[0], header[1])
      self.end_headers()
      if isinstance(data.response, str):
        self.wfile.write(data.response.encode("utf-8", "replace"))
      elif isinstance(data.response, htmldoc):
        self.wfile.write(data.response.render().encode("utf-8", "replace"))
      else:
        self.wfile.write(data.response)


    def do_POST(self):
      pass
      
    

server = HTTPServer(("0.0.0.0", 4567), WebRequestHandler)
server.serve_forever()