#!/usr/bin/env python
# Log and sort the times of individual tests when run from Maven

import math, operator, re, sys

if len(sys.argv) != 2:
	print "Usage: {0} logfile".format(sys.argv[0])
else:
	logfile = sys.argv[1]
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
	tt = sorted(zip(tests, times), key=operator.itemgetter(1), reverse=True)
	for t, e in tt:
		total += e
		print "{0} {1}s".format(t.ljust(70, '.'), str(e).rjust(6))

	print "\nRun: {0} tests in {1}mins {2}s (file: {3})".format(len(tt), int(total / 60), int(total % 60), logfile)
	