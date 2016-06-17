from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import os

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        message = '\n'.join([
          'CLIENT VALUES:',
          'client_address=%s (%s)' % (self.client_address, self.address_string()),
          'command=%s' % self.command,
          'path=%s' % self.path,
          'real path=%s' % parsed_path.path,
          'query=%s' % parsed_path.query,
          'request_version=%s' % self.request_version,
          '',
          'SERVER VALUES:',
          'server_version=%s' % self.server_version,
          'sys_version=%s' % self.sys_version,
          'protocol_version=%s' % self.protocol_version,
          '',
        ])

	#print parsed_path.path

	#str = os.popen("home/hackathon/source/hackathon/cdr/upload_cdr.pl").read()
    	#consoleLog( "info", str)
	
	str = os.popen("python /home/hackathon/source/hackathon/recognition/baidu.py  /home/hackathon/source/hackathon/record/" + parsed_path.path[1:] +".wav").read()
	print str


        self.send_response(200)
        self.end_headers()

        self.wfile.write(message)

        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 8000), GetHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
