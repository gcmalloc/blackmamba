from blackmamba import *
from blackmamba.client import statistics as stats
from foolib.parse import *
import sys, time

def save(response):
    import hashlib
    name = '/tmp/out/' + hashlib.sha1(response).hexdigest()
    if DEBUG: print "%s bytes read:" % len(response), name
    with open(name, 'wb') as fh: 
        fh.write(response)


class HTTP(object):
	""" 
	An implimentation of the HTTP protocol as an example of using this library and coroutines
	"""

	def __init__(self, host, path='/', verb='GET', port=80):
		self.host = host
		self.port = port
		self.path = path
		self.verb = verb
		self.headers = {}
		self.cookies = {}
		self.data = ""

	def __str__(self):
		self.headers['Host'] = self.host
		if self.cookies:
			self.headers['Cookie'] = djoin(self.cookies, '; ', '=')
		if self.data:
			self.headers['Content-Length'] = str(len(self.data))
		request = []
		request.append("%s %s HTTP/1.1" % (self.verb, self.path))
		request.append(djoin(self.headers, '\r\n', ': '))
		request.append("")
		request.append(self.data)
		return "\r\n".join(request)
		
	
	def run(self):
		""" 
		A coroutine to define the read/write interation with the target host.
		Every read/write must yield.
		"""
		yield connect(self.host, self.port, 5)
		yield write(self.__str__())
		response = yield read()
		yield close()


def httpgen(host, count):

	for i in xrange(count):
		yield HTTP(host).run()


if __name__=='__main__':

	host = sys.argv[1]
	count = int(sys.argv[2])
	
	start = time.time()
	run(httpgen(host, count))
	end = time.time()

	print '\n-- statistics --\n'
	for k,v in stats.items():
		print '%s : %s' % (k,v)

	completed = stats['Completed']
	print "%i connections completed in %.3f seconds (%.3f per sec)\n" % (completed, end-start, completed/(end-start)) 


