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


import appUtil
import myUtility
import json
import sys
import datetime
import math

def weedOutToday(ls):
	for e in ls:
		#checks if last read today (no need to read more than once a day)
		#if (e.lastRead - datetime.datetime.today()) >  datetime.datetime.timedelta(days = 1):
		if e.lastRead == datetime.datetime.today().date():
			ls.remove(e)
	return ls

myUtility.CheckArgs(2, "<in/all file> <out/sample file>")

EntryList = appUtil.EntryListFromJsonFile(sys.argv[1])
EntryList = weedOutToday(EntryList)

appUtil.printList(EntryList[:10])

for e in EntryList:
	if e == "667728512":
		print "Looking for : "
		appUtil.printList([e])


if(len(EntryList) == 0):
	print "No new apps"
	sys.exit(0)

#sample = int(math.ceil(len(EntryList)/6.0))
sample = 999
if sample > 1000:
	sample = 999

EntryList = appUtil.SortByDate(EntryList)

print "\n"
appUtil.printList(EntryList[:10])

SampleList = EntryList[:sample]

#appUtil.printList(SampleList)

print len(SampleList)

myUtility.OverwriteFile(sys.argv[2], "")
for el in SampleList:
	myUtility.AppendToFile(sys.argv[2], el.id +"\n")


