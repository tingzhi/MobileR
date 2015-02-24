'''
   Copyright 2015 Kendall Bailey

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

'''


import re
import sys

if len(sys.argv) != 3:
	print "Error: basicRegex <pattern> <infile>"
	print "length = " + str(len(sys.argv))
	sys.exit(2)

try:
	pat = re.compile(sys.argv[1])
except SyntaxError:
	print "Not a valid regex pattern"
	sys.exit(2)

try:
	f = open(sys.argv[2])
except IOError as e:
	print "Problem opening file {2}. Error ({0}) : {1}".format(e.errno, e.strerror, sys.argv[2])
	sys.exit(2)

lines = f.readlines()
f.close

count = 0
for l in lines:
	#print l
	#print pat.pattern
	m = pat.findall(l)
	if m:
		for mat in m:
			print mat
			count = count + 1

