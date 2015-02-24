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
import json
import sys


if len(sys.argv) != 3:
        print "Error: basicRegex <infile> <outfile>"
        print "length = " + str(len(sys.argv))
        sys.exit(2)


try:
        f = open(sys.argv[1])
except IOError as e:
        print "Problem opening file {2}. Error ({0}) : {1}".format(e.errno, e.strerror, sys.argv[1])
        sys.exit(2)

text = f.read()
f.close

pat = re.compile('{.*}')
ls = pat.findall(text)

#get name of the new file
patName = re.compile("\"nameRaw\":\".*?\"")
name = re.search(patName, ls[1])
namestr =  name.group()
namestr = namestr.replace(" ", "")
namestr = namestr[11:-1]

illegalchars = "[:\\\\/*?|<>]"
#print "old name " +  namestr
for char in illegalchars:
	namestr.replace(char, "_")
namestr = re.sub(r"[\W+]", "_", namestr)

namestr = namestr[0:15]
#print "NewName " + namestr

namestr2 = sys.argv[1][12:-4]

with open(sys.argv[2] + namestr2 + ".json", 'w') as outfile:
	outfile.write(json.dumps(json.loads(ls[1]), indent =4))
	outfile.close()	
