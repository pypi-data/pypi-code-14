import argparse, socket

parser = argparse.ArgumentParser(prog = 'recv', description = 'Recv file.')
parser.add_argument('-b', '--buffer', type = int, dest = 'buffer', default = 1024)
parser.add_argument('-l', '--listen', type = str, dest = 'listen', default = '0.0.0.0')
parser.add_argument('-p', '--port', type = int, dest = 'port', default = 7878)
parser.add_argument('-a', '--accept', type = str, dest = 'accept')
parser.add_argument('-v', '--verbose', action = 'store_true')
parser.add_argument('output', type = str)
args = parser.parse_args()

dump = open(args.output, 'wb')
address = (args.listen, args.port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(address)
s.listen(1)

if args.verbose:
	print('Listening on %s:%d' % address)

while True:
	c, address = s.accept()
	
	if args.verbose:
		print('Client connected: %s:%d' % address)
	
	if args.accept is None or address == args.accept:
		break

if args.verbose:
	print('Client acctepted: %s:%d' % address)

total = 0

while True:
	chunk = c.recv(args.buffer)
	total += len(chunk)

	if args.verbose:
		print('\rReceived %d bytes' % total, end = '')
	
	dump.write(chunk)
	if not chunk:
		break

if args.verbose:
	print('\nDone')
