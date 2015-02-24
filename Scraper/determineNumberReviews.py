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
import numpy


def getNumberTotalReviews(jsonlist, id):
	num = 0
	if id in jsonlist:
		ind = jsonlist.index(id)
		num = jsonlist[ind].numReviews
		num = int(numpy.ceil(num/10.0))
		if num > 100:
			num = 100
		#print "Total Number Reviews: " + str(jsonlist[ind].numReviews) + " Pages: " + str(num) 
	return num


def getNumberNewReviews(jsonlist, id):
	num = 0
	if id in jsonlist:
		ind = jsonlist.index(id)
		num = jsonlist[ind].newReviews
		num = int(numpy.ceil(num/10))
		if num > 100:
			num = 100
		print "Total New Reviews: " + str(jsonlist[ind].newReviews) + " Pages: " + str(num) 
	return num

def main():
	myUtility.CheckArgs(2, "<master id list> <id number>")

	elist = appUtil.EntryListFromJsonFile(sys.argv[1])
	id = str(sys.argv[2]) 

	#print id
	#print id in elist
	print getNumberTotalReviews(elist, id)
	


if __name__ == "__main__":
	main()
