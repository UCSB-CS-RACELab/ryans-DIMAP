# Backup Server
# Author: Ryan Halbrook
# Date: 3/3/15
# references: http://pymotw.com/2/BaseHTTPServer/
#	      https://wiki.python.org/moin/BaseHttpServer
#

import BaseHTTPServer
import cgi
import time
from subprocess import call
from socket import gethostname;

PORT_NUMBER = 8080
HOST_NAME = gethostname() # internal hostname

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
	s.send_response(200)
	s.send_header("Content-type", "text/html")
	s.end_headers()
    def do_GET(s):
	s.send_response(200)
	s.send_header("Content-type", "text/html")
	s.end_headers()
	s.wfile.write("<html>\n<head><title>Backup Server Test</title></head>\n")
	s.wfile.write("<body>\n<p>Test</p>\n")
	s.wfile.write("<p>You accessed path: %s</p>\n" % s.path)
	s.wfile.write("</body>\n</html>\n")
    def do_POST(s):
	# Parse the form data posted
        form = cgi.FieldStorage(
            headers=s.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':s.headers['Content-Type'],
                     })

	if 'cmd' not in form or 'code' not in form:
	    s.send_error(400)
	    return	
	if form['code'].value != '1547':
	    s.send_error(401)
	    return


	cmd = form['cmd'].value
	print "Command: %s" % cmd
	if cmd == "restore-new-machine":
	    if 'machine' not in form or 'jobid' not in form:
		s.send_error(400)
		return
	    ip = form['machine'].value
	    jobid = form['jobid'].value
	    print "preparing to restore new machine: %s" % ip
	    bash_command="./restore-new-machine -m %s -j %s" % (ip, jobid)
	    print "command = %s" % bash_command
	    call(["/home/ec2-user/restore-new-machine.sh", "-m", ip, "-j", jobid])

        # Begin the response
        s.send_response(200)
        s.end_headers()
        s.wfile.write('Client: %s\n' % str(s.client_address))
        s.wfile.write('User-agent: %s\n' % str(s.headers['user-agent']))
        s.wfile.write('Path: %s\n' % s.path)
	
        return

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Started at %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stopped at %s:%s" % (HOST_NAME, PORT_NUMBER)



