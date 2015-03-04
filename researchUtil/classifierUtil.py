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
from nltk.corpus import stopwords
from nltk.stem import porter
from nltk.stem.porter import *
import os
from researchUtil import myUtility
from researchUtil import appUtil



revStopWordsFile = "stop-words_english_4_en.txt"
rnStopWordsFile = "stop-words_english_3_en.txt"
mobileStopWordsFile = "MobileStopWords.txt"

def applyJunkGrammar(lines):
	ret = []
	for el in lines:
		if (re.match("^\s*[A-Z\s\&]*$", el) or
			re.match ("^.*:\n$", el) or
			re.match ("^\s*([A-Z]([a-z])+\s*){2,}$",el) or
			re.match ("^\s*([A-Z]([a-z])+\s*)+(and|or|\&)(\s*[A-Z]([a-z])+\s*)+", el)):
			#print el
			i = 1 + 1
		else:
			ret.append(el)
	return ret



#takes list of sentences returns list of list words in sentence
def preProcLines(lines, HasHeaders, stopfilename):
	ret = []
	if HasHeaders == True:
		lines = applyJunkGrammar(lines)
	for l in lines:
		try:
			if not isinstance(l, unicode):
				newl = unicode(l, 'utf-8') #forces everything to unicode
			else:
				newl = l
			newl = newl.encode("ascii", "ignore") #gets rid of those 'cute' pain in the ass bullets
			newl = newl.lower()
			newl = re.sub('[^a-zA-z @]', "", newl)
			ret.append(newl)
       #maybe remove duplicates??
#	print ret
		except Exception as err:	
			print "Problem with string : " + l
			print type(l)
			raise err
	ret = removeStopWords(ret, stopfilename)
#       print "\n\n\n\n"
#	print ret
	return ret

#takes list returns list
def removeStopWords(text, stopWordsFile):
        #text is a ls
	ret = []
	stopfile = open(stopWordsFile, 'r')
	stoplist = stopfile.read().split('\r\n')
	stopfile.close()
	
	mstopfile = open(mobileStopWordsFile, 'r')
	mobilestoplist = mstopfile.read().split("\n")
	mstopfile.close()

#	print "Remove Stop Words length = " + str(len(text))
	stemmer =  PorterStemmer()       
	i = 0
	for l in text:
		line = l.split(" ")
		statement = []
		for w in line:
			if w not in stoplist and re.sub('\s',"", w) !=  "" and w not in mobilestoplist:
				w = stemmer.stem(w)
				statement.append(w)
#		if statement == []:
#			print i
#			print text[i]
#			print l
		ret.append(statement)
		i = i + 1
        #returns list
	return ret



#takes filename of meis reviews in json returns list of list words in sentences
def getCorpusMeiRevJson(filename, path):
	ret = []
	objls = appUtil.MeiRevFromJsonFile(path + filename)
	for el in objls:
		ret.append(el.title + " :: " + el.text)
	#problem is here V
	print "Classutil ret length 1 - " + str(len(ret))
	ret = preProcLines(ret, False, rnStopWordsFile)
	print "Classutil ret length 2 - " + str(len(ret))
	return ret

#takes filename returns list of list words in sentences
def getReviewCorpus(filename, path):
	ret = []
	objls = appUtil.ReviewFromJsonFile(path + filename)
	for el in objls:
		ret.append(el.title + " :: " + el.text)
	contents = preProcLines(ret, False, revStopWordsFile)
	return contents

#takes filename returns list of list words in sentences
#removes headers
def getCorpus(filename, path):
	ret = []
	contents = myUtility.ReadFileLines(path+filename)
	contents = preProcLines(contents, True, rnStopWordsFile)
	return contents


def getAllCorpusInFolder(path):
	ret = []
	files = os.listdir(path)
	for f in files:
		ret = ret + getCorpus(f, path)
	return ret


