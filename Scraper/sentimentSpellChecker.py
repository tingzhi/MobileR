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
import myUtility
import enchant #spell checking library -> is english?
import re
import sys
import fuzzywuzzy
from fuzzywuzzy import fuzz

engDict = enchant.Dict("en_US")

def init_Dictionary():
	mwords = myUtility.ReadFileLines("mobileWords.txt")
	for w in mwords:
		if not engDict.is_added(w):
			engDict.add(w)
	rpmts = myUtility.ReadFileLines("myrecommendations.txt")
	for w in rpmts:
		el = w.split("\t")
		engDict.store_replacement(el[0], el[1])
	

def checkWord(strn):
	return engDict.check(strn)

def sentiSpell(strn):
	try:
		corrected = spellCheck_Replace(strn)
		return corrected
	except ValueError as valer:
		"Index error:", valer
	except:
		"Unexpected error:", sys.exc_info()[0]
		return strn
		

def spellCheck_Replace(strn):
	ret = ""
	ls = strn.split(" ")
	for el in ls:
		if engDict.check(el) == True: #if word in English Dictionary
			ret = ret + " " + el
		else:
			#try other spellings - just take best match 
			if engDict.suggest(el) != []:
				sug = engDict.suggest(el)[0]
				no3dups = el
				no2dups = el
				regx = re.compile(r'(\w)\1+', re.IGNORECASE) #looks for duplicate letters
				numdups = sum(1 for _ in regx.finditer(el)) #iterable is not permanent, so no use declaring a variable for it
				dupInstances = []
				if numdups > 0:	
					for match in regx.finditer(el):
						#only replace the first instance, all others will be taken care of in time
						no3dups = re.sub(match.group(),match.group()[0] +  match.group()[0], no3dups, 1)
						no2dups = re.sub(match.group(),match.group()[0], no2dups, 1)
						#replace duplicates with a single set of duplicates, because that is natural.
						dupInstances.append([match.start(), match.group()])
				#	dupInstances.append([len(no3dups), ""]) #this is an end marker
				#	if engDict.check(no3dups) == False:
				#		no2dups = re.sub(match.group(),match.group()[0], el, 1)
				#		if engDict.check(no2dups) == False:
				#			sug2 = engDict.suggest(no2dups)[0] #run loop again on suggestion
				#		else:
				#			sug2 = no2dups
				#	else:
				#		sug2 = no3dups
					sug2 = getBestMatch(el, no3dups, no2dups)
					return BuildString(sug2, regx, dupInstances)
				else:
					ret = ret + " " + sug 
						
			else: #if not really a word and not suggestable, just take it... :C
				ret = ret + " " + el
	return ret


def getBestMatch(orig, twoDups, nodups):
	ret = ""
#	print orig

	if engDict.check(twoDups) == True: #if in dictionary, just return
		return twoDups
	if engDict.check(nodups) == True:
		return nodups
	
	sug2dups = engDict.suggest(twoDups)[0] #run loop again on suggestion
	sugNoDups = engDict.suggest(nodups)[0] #run loop again on suggestion
	
	r2dups = fuzz.ratio(orig, sug2dups)
	rNoDups = fuzz.ratio(orig, sugNoDups)
	
#	print orig + "\t" + twoDups + "\t" + sug2dups + "\t" + str(r2dups)
#	print orig + "\t" + nodups + "\t" + sugNoDups + "\t" + str(rNoDups)
	
	if r2dups > rNoDups:
		return sug2dups
	else:
		return sugNoDups 	

	

def BuildString(sugstr, regx, dupInstances):
	s = re.search(regx, sugstr)
	if dupInstances == []: #no more streching suggestions
		return sugstr


	if s and s.start() <= dupInstances[0][0]: #original word had duplicate letters
	#if s:
		lengPropMatch = len(s.group())
		lengDups = len(dupInstances[0][1])
		if s.group()[0] == dupInstances[0][1][0]:
			lengDiff = lengDups - lengPropMatch
			if (lengDiff > 1) : #if the length difference is 2 or more
				partkeep = sugstr[:s.start()] + dupInstances[0][1]
				index = s.end()
			#	index = lengPropMatch+s.start()
		#		print "S.end = " + str(s.end()) + " Index " + str(index)
		#		print "Sug Str - " +  sugstr + " Dup Instances after",
			#	print dupInstances
				dupInstances = map(lambda x: [x[0]-(index + (s.end() - s.start())), x[1]], dupInstances)
		#		print "Sug Str - "+ sugstr + " Dup Instances after",
		#		print dupInstances
				return partkeep + BuildString(sugstr[index:], regx, dupInstances[1:]) #Then sentiment! keep multiples
			else: #misspelling -> correct
				partkeep = ""
				index = 0
				sub = 0

				if lengDiff == 0: #same length, no problem
					index = s.start()+len(s.group())
				else:
					index = s.start()+2#correct misspelling, needs a double letter
					sub = 1

				partkeep = sugstr[:index]
				
				dupInstances = map(lambda x: [x[0]-(index+sub), x[1]], dupInstances)
				return partkeep + BuildString(sugstr[index:], regx, dupInstances[1:]) 
		else: #not matching duplicates, move to next part
			#keep dup instances
			index = s.start()+len(s.group())
			partkeep = sugstr[:index]
		#	print sugstr + "   ind " + str(index) + "len " + str(len(sugstr))	
			if len(sugstr) <= index: #got wrong word, just return it
				return sugstr
			return partkeep + BuildString(sugstr[:index], regx, dupInstances)
	else: #A single letter is duplicated
		#print "Sug str - " + sugstr + " dup instance " + str(dupInstances[0][0])
		if len(dupInstances[0][1]) > 2 and sugstr[dupInstances[0][0]] == dupInstances[0][1][0]: #not misspelling and same letter extended
			strnl = sugstr[:dupInstances[0][0]]
			strnr = sugstr[dupInstances[0][0]+1:]
			partkeep = strnl + dupInstances[0][1]
			return partkeep + BuildString(strnr, regx, dupInstances[1:])
		else: #fix misspelling
			return BuildString(sugstr, regx, dupInstances[1:])








