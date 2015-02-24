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
import json
import sys
import re
import appUtil
import myUtility
import os.path

myUtility.CheckArgs(2, "<entry list> <todays list>")


elist = appUtil.EntryListFromJsonFile(sys.argv[1])

current = myUtility.ReadFileLines(sys.argv[2])

#appUtil.printList(elist)
ls = []

for el in current:
	el = el.strip("\n")
	ls.append(el.split(" "))

uls = []
for el in ls:
	if str(el[0]) in elist and str(el[0]) not in uls:
		ind = elist.index(str(el[0]))
		elist[ind].updateReading(int(el[1]), "0")
		uls.append(str(el[0]))
		print str(el[0])


strlist = []
for el in elist:
	strlist.append(el.toJsonStr())

print strlist[:15]

#myUtility.OverwriteJsonListToFile(sys.argv[1], strlist)
