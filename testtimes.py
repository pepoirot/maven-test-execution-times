#!/usr/bin/env python
# Log and sort the times of individual tests when run from Maven

import math, operator, re, sys

def order_test_times(logfile):
	"""Parse and order test times from longest to shortest.
	"""
	p = list(re.compile(p) for p in ['(?<=Running )[A-Za-z.]+Test', '(?<=Time elapsed: )[0-9.]+(?! sec)'])
	tests = []
	times = []
	match = False

	with open (logfile, 'r') as log:
		for line in log:
			if match:
				m = p[1].search(line)
				if m is not None:
					times.append(float(m.group(0)))
					match = False
			else:
				m = p[0].search(line)
				if m is not None:
					tests.append(m.group(0))
					match = True

	total = 0
	td = sorted(zip(tests, times), key=operator.itemgetter(1), reverse=True)
	for t, e in td:
		total += e
		print "{0} {1}s".format(t.ljust(70, '.'), str(e).rjust(6))

	print "\nRun: {0} tests in {1}mins {2}s (file: {3})".format(len(td), int(total / 60), int(total % 60), logfile)
	return td, total
	
def simple_distribution(td, total, target):	
	"""Simple round-robin distribution of the tests assuming a presorted list of tests,
	   and perfect parallelisation (p=1 in Amdahl's law).
	"""
	n = int(math.ceil(total / (target * 60)))
	buckets = [[] for b in range(n)]

	print "\nExample of test distribution to run in {0} mins:".format(target)

	for t in range(len(td)):
		buckets[t % n].append(td.pop())
	for b, bucket in enumerate(buckets):
		print "\n* Bucket", b + 1
		for t in bucket:
			print t[0]

if __name__ == "__main__":
	if len(sys.argv) == 2:
		order_test_times(sys.argv[1])
	elif len(sys.argv) == 3:
		td, total = order_test_times(sys.argv[1])
		simple_distribution(td, total, int(sys.argv[2]))
	else:
		print "Usage: {0} logfile [desired runtime in mins]".format(sys.argv[0])