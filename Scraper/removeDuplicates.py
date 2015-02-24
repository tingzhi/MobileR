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


import os
import sys
import myUtility
import appUtil
from collections import Counter

'''load list
	do a counter for all things greater than 1 frequency
	create empty list for duplicates
	create an empty list for writing
	go through each element of the list
	if it is in the counter, put it in the duplicate list
	if already in the duplicate list compare the two and keep the youngest
	combine the lists and write to file

'''

def GetYoungest(ent1, dupls):
	#return youngest
	ind = dupls.index(ent1.id)
	ent2 = dupls[ind]

	print ent2.id + " " + str(ent2.lastRead)
	print ent1.id + " " + str(ent1.lastRead)

	if ent2.lastRead < ent1.lastRead:
		dupls[ind] = ent1
	
	return dupls



def main():
	myUtility.CheckArgs(2, "<master Entry List> <outfile>")
	ls = appUtil.EntryListFromJsonFile(sys.argv[1])

	strls = []
	for el in ls:
		strls.append(str(el))

	ctr = Counter(strls)
	strls =[]
	for el in ctr.most_common():
		if el[1] > 1:
			strls.append(el[0])

	print "Beginning length: " + str(len(ls))

	dupls = []
	finals = []

	for el in ls:
		if el in strls and el not in dupls:
			dupls.append(el)
		elif el in strls and el in dupls:
			dupls = GetYoungest(el, dupls)
		else:
			finals.append(el)


	finals = finals + dupls
	print "End length : " + str(len(finals))
	

	strls = []
	for el in finals:
		strls.append(str(el))
	ctr = Counter(strls)
	print ctr.most_common(10)
	
	jsonls = []
	for el in finals:
		jsonls.append(el.toJsonStr())
	myUtility.OverwriteStrListToFile(sys.argv[2], jsonls)	

	


if __name__ == "__main__":
	main()
