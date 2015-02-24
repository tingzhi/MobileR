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
import sys
import appUtil
import myUtility
import re
from collections import Counter



def ExtractId(url):
	l = url.encode("ascii", "ignore")
	m = re.search('id\d+',l)
	if m:
		l = m.group(0)
		n = re.search('\d{5,}', l)
		print "N - " + n.group(0)
		return n.group(0)
	else:
		print "NO MATCH " + l

def addNewIds(idls, filename):
	entryList = appUtil.EntryListFromJsonFile(filename)
	retls = []
	for el in idls:
		if el not in entryList:
			retls.append(el)
	return retls

myUtility.CheckArgs(2, "<new ids> <master Id File>")

urls = myUtility.ReadFileLines(sys.argv[1])


idls = []
for l in urls:
	id = ExtractId(l)
	idls.append(id)

ctr = Counter(idls)
print ctr.most_common(2)
idls = list(set(idls))


newids = addNewIds(idls, sys.argv[2])
newEnt = []
for el in newids:
	ent = appUtil.Entry(str(el))
	newEnt.append(ent.toJsonStr())

print len(newEnt)

myUtility.AppendJsonListToFile(sys.argv[2], newEnt)
