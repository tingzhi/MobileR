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
from abc import ABCMeta, abstractmethod
import json
import sys
import datetime
import re
import guess_language #for language prediction!
import goslate
import langid
import myUtility
import emojiDict

class researchData:
	__metaclass__ = ABCMeta

	@abstractmethod
	def toJsonStr(): pass
	
	@abstractmethod
	def fromJson(): pass

	
	def replace_emojis(self, strn):
		ret = strn
		emojis = re.findall (r'\xf0\x9f..', ret)
		for e in emojis:
			ret = re.sub(e, emojiDict.emojiToEmoticon[e], ret)
		return ret
	
	def clean_text(self, strn):
		#TODO Check english
		#	spell check
		ret = self.replace_emojis(strn)
		ret = ret.replace("\\", "\\\\")
		ret = ret.replace("\"", "\\\"")
		ret = ret.replace("\n\r", " ")
		ret = ret.replace("\r", " ")
		ret = ret.replace("\n", " ")
		ret = ret.replace("\t", " ")
		ret = re.sub('\\\*\"', '\\\"', ret) #This gets rid of extra slashes

		ret = re.sub('\s{2,}', ' ', ret) # this get rid of large spaces
		ret = ret.replace("<semicolon>", ";") #for translating from the csv, there were some storage errors
		ret = re.sub('[^\x00-\x7F]', "", ret) #gets rid of things outside of ascii
		return ret

	def check_Language(self, strn):
	#	gs = goslate.Goslate()
	#	if len(strn) < 20:
	#		while len(strn) < 20:
	#			strn = strn + " " + strn
	#	lang = guess_language.guessLanguage(strn)
		lang = langid.classify(strn[:100])[0]
	#	lang = gs.detect(strn[:100])
		if lang != 'en':
			raise Exception("AppUtil.MeiRev - Not English Submission " + strn + " Language - " + str(lang) )



	
'''	def cleanReleaseNotes(self, notes):
		ret = notes.replace('\n','\\n')
		ret = ret.replace('\r','\\r') #only rn
	#	ret = ret.replace('\t','\\t')
		ret = ret.replace('\"', '\\"')
		ret = ret.replace('\(', '\\(') #only rn
		ret = ret.replace('\)', '\\)') #only rn
		
		return ret
'''


class Entry:
	def __init__ (self, idnum):
		self.id = idnum
		self.lastRead = datetime.datetime(1901, 1, 1, 0, 0)
		self.numReviews = 0
		self.lastVersion = "0"
		self.newReviews = 0

	def fromJson(self, jsonStr):
		data = json.loads(jsonStr)
		self.id = json.dumps(data["id"]).strip('\"')
		self.lastRead = datetime.datetime.strptime(data["lastRead"], "%m-%d-%Y")
		self.numReviews = data["numReviews"]
		self.lastVersion = data["lastVersion"]
		self.newReviews = data["newReviews"]

	def toJsonStr(self):
		jsonStr = "{\"id\":\"" + self.id + "\",\"numReviews\":"
		jsonStr = jsonStr + str(self.numReviews) + ",\"lastRead\":\""
		jsonStr = jsonStr + self.lastRead.date().strftime('%m-%d-%Y') +"\",\"newReviews\":"
		jsonStr = jsonStr + str(self.newReviews) + ",\"lastVersion\":\""
		jsonStr = jsonStr + self.lastVersion + "\"}"
		return jsonStr

	def __eq__(self, other):
		return self.id == other.id

	def __eq__(self, str):
		return self.id == str

	def __str__(self):
		return self.id

	def convertDate(self, todaysDate):
		return todaysDate

	def updateReading(self, numRevs, lastVersion):
		self.lastRead = datetime.datetime.today()
		print self.id + " Old Reviews: " + str(self.numReviews) + " New Reviews: " + str(numRevs) + " Difference: " + str(numRevs - self.numReviews)
		self.newReviews = numRevs - self.numReviews
		self.numReviews = numRevs
		return

class HistoryEntry:
	def __init__(self):
		self.date = datetime.datetime.min
		self.notes = ""
		self.id = ""

	def cleanReleaseNotes(self, notes):
		ret = notes.replace('\n','\\n')
		ret = ret.replace('\r','\\r')
		ret = ret.replace('\t','\\t')
		ret = ret.replace('\"', '\\"')
		ret = ret.replace('\(', '\\(')
		ret = ret.replace('\)', '\\)')
		return ret

	def fromJson(self, jsonStr):
		data = json.loads(jsonStr)
		self.date = datetime.datetime.strptime(data["releaseDate"], "%Y-%m-%d %H:%M:%S")
		if data.get('releaseNotes'):
			self.notes = self.cleanReleaseNotes(data["releaseNotes"])
		self.id = data["versionString"]

	def fromItunesJson(self, jsonStr):
		data = json.loads(jsonStr)
		self.date = datetime.datetime.strptime(data["releaseDate"], "%Y-%m-%dT%H:%M:%SZ")
		if data.get('releaseNotes'):
			self.notes = self.cleanReleaseNotes(data["releaseNotes"])
		self.id = data["versionString"]
		
	def toJsonStr(self):
		jsonStr = "{\"versionString\":\"" + self.id + "\",\"releaseNotes\":\""
		jsonStr = jsonStr + self.notes + "\",\"releaseDate\":\""
		jsonStr = jsonStr + str(self.date) + "\"}"
		return jsonStr

	def __eq__(self, other):
		return self.id == other.id
	
	def __eq__(self, str):
		return self.id == str

class Review(researchData):
	def __init__(self):
		self.title = ""
		self.rating = ""
		self.user = ""
		self.versionNumber = ""
		self.date = datetime.datetime.min
		self.body = ""
		self.pctHelp = 0
		self.helpVotes = 0
		self.totalVotes = 0
		self.userLink = ""
		self.id = ""
		self.country = ""
		self.labels = []

	def __eq__(self, other):
		return self.id == other.id

	def __eq__(self, str):
		return self.id == str
	
	def toJsonStr(self):
		jsonStr = "{\"title\":\"" + self.clean_text(self.title) + "\",\"rating\":\""
		jsonStr = jsonStr + self.rating + "\",\"user\":\""
		jsonStr = jsonStr + self.clean_text(self.user) + "\",\"versionNumber\":\""
		jsonStr = jsonStr + self.versionNumber + "\",\"date\":\""
		jsonStr = jsonStr + str(self.date) + "\",\"text\":\""
		jsonStr = jsonStr + self.clean_text(self.text) + "\",\"percentHelpful\":"
		jsonStr = jsonStr + str(self.pctHelp) + ",\"helpfulVotes\":"
		jsonStr = jsonStr + str(self.helpVotes) + ",\"totalVotes\":"
		jsonStr = jsonStr + str(self.totalVotes) + ",\"userLink\":\""
		jsonStr = jsonStr + self.userLink + "\",\"reviewId\":\""
		jsonStr = jsonStr + self.id + "\",\"country\":\""
		jsonStr = jsonStr + self.country + "\",\"labels\":"
		jsonStr = jsonStr + json.dumps(self.labels) + "}"
		return jsonStr.encode("ascii", "ignore")

	def replace_emojis(self, strn):
		return super(Review, self).replace_emojis(strn)

	def check_Language(self, strn):
		super(Review, self).check_Language(strn)	

	def remove_json_breakers(self, strn):
		ret = strn.replace("\n", " ")
		ret = ret.replace("\r", " ")
		ret = ret.replace("\r\n", " ")
		return ret
	

	def clean_text(self, strn):
		return super(Review, self).clean_text(strn)
		#TODO Check english
		#	spell check
		ret = self.replace_emojis(strn)
		ret = ret.replace("\\", "\\\\")
		ret = ret.replace("\n\r", " ")
		ret = ret.replace("\r", " ")
		ret = ret.replace("\"", "\\\"")
		ret = re.sub('\\\*\"', '\\\"', ret) #This gets rid of extra parenthesis
		ret = ret.replace("\t", " ")
		return ret

	
	def fromItunesJson(self, jsonStr):
		try:
			data = json.loads(jsonStr)
			self.title = self.clean_text(data["title"])
			self.rating = data["rating"]
			self.user = self.clean_text(data["user"])
			self.versionNumber = data["versionNumber"]
			if data["date"] ==  "":
				self.date = datetime.datetime.strptime(data["versionNumber"], "%b %d, %Y")
				self.versionNumber = "0"
			else:
				self.date = datetime.datetime.strptime(data["date"], "%b %d, %Y")
			self.text = self.clean_text(data["text"])
			if data["totalVotes"] == "":
				self.pctHelp = 0
				self.helpVotes = 0
				self.totalVote = 0
			else:	
				self.pctHelp = data["percentHelpful"]
				self.helpVotes = data["helpfulVotes"]
				self.totalVote = data["totalVotes"]
			self.userLink = data["userLink"]
			self.id = data["reviewId"]
			self.country = data["country"]
			if "labels" in data:
				self.labels = data["labels"]
		except ValueError:
			print "AppUtil.Review - Value error:", sys.exc_info()[0], " in: "
			print jsonStr
		except:
			print "AppUtil.Review - Unexpected error:", sys.exc_info()[0], " in: "
			print jsonStr
		
	def fromJson(self, jsonStr):
		try:
			newStr = self.remove_json_breakers(jsonStr)
			data = json.loads(newStr)
			self.title = self.clean_text(data["title"])
			self.rating = data["rating"]
			self.user = self.clean_text(data["user"])
			self.versionNumber = data["versionNumber"]
			self.date = datetime.datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S")
			self.text = self.clean_text(data["text"])
			self.pctHelp = data["percentHelpful"]
			self.helpVotes = data["helpfulVotes"]
			self.totalVote = data["totalVotes"]
			self.userLink = data["userLink"]
			self.id = data["reviewId"]
			self.country = data["country"]
			if "labels" in data:
				self.labels = data["labels"]
		except ValueError:
			print "AppUtil.Review - Value error:", sys.exc_info()[0], " in: "
			print jsonStr
		except Exception as err:
			print "AppUtil.Review - Unexpected error:", sys.exc_info()[0], " ", err,  " in: "
			print jsonStr
			print newStr
			


	def __str__(self):
		return self.id

	def Print(self):
		return self.text


class MeiRev(researchData):

	def __init__(self):
		self.appName = ""
		self.title = ""
		self.text = ""
		self.versionNumber = ""
		self.labels = ""
		self.date = datetime.datetime.min
	
	def check_Language(self, strn):
		super(Review, self).check_Language(strn)	
		return
	#	gs = goslate.Goslate()
	#	if len(strn) < 20:
	#		while len(strn) < 20:
	#			strn = strn + " " + strn
#		lang = guess_language.guessLanguage(strn)
		lang = langid.classify(strn[:100])[0]
	#	lang = gs.detect(strn[:100])
		if lang != 'en':
			raise Exception("AppUtil.MeiRev - Not English Submission " + strn + " Language - " + str(lang) )
	
	
	def replace_emojis(self, strn):
		return super(MeiRev, self).replace_emojis(strn)

	def clean_text(self, strn):
		ret = self.replace_emojis(strn)
		ret = ret.replace("\\", "\\\\")
		ret = ret.replace("\"", "\\\"")
	#	ret = ret.replace('\xe2\x80\xa6', "...")
		ret = re.sub('\\\*\"', '\\\"', ret) #This gets rid of extra parenthesis
		ret = ret.replace("\t", " ")
		ret = ret.replace("\n", " ")
		ret = re.sub('\s{2,}', ' ', ret) # this get rid of large spaces
		ret = ret.replace("<semicolon>", ";") #for translating from the csv, there were some storage errors
		ret = re.sub('[^\x00-\x7F]', "", ret)
		return ret


	def fromCSVrowLs(self, ls):
		try:
			self.check_Language(ls[2])

		except Exception as err:
			raise err	
		self.appName = self.clean_text(ls[0])
		self.title = self.clean_text(ls[1])
		self.text = self.clean_text(ls[2])
		self.versionNumber = self.clean_text(ls[3])
		self.labels = self.clean_text(ls[4])
		self.date = datetime.datetime.strptime(ls[7], "%Y-%m-%d")

	def fromJson(self, jsonstr):
		try:
			data = json.loads(jsonstr)
		except ValueError as err:
			print "Problem with string : " + jsonstr
			raise err
		try:
			self.check_Language(data["text"])
		except Exception as err:
			raise err	
	
		self.appName = self.clean_text(data["appName"])
		self.title = self.clean_text(data["title"])
		self.text = self.clean_text(data["text"])
		self.versionNumber = data["versionNumber"]
		self.labels = data["tags"]
		self.date = datetime.datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S")

	def toJsonStr(self):
		try:
			jsonStr = "{\"title\":\"" + self.clean_text(self.title) + "\",\"appName\":\""
			jsonStr = jsonStr + self.clean_text(self.appName) + "\",\"versionNumber\":\""
			jsonStr = jsonStr + self.versionNumber + "\",\"date\":\""
			jsonStr = jsonStr + str(self.date) + "\",\"text\":\""
			jsonStr = jsonStr + self.clean_text(self.text) + "\",\"tags\":\""
			jsonStr = jsonStr + self.clean_text(self.labels) +  "\"}"
			return jsonStr.encode("ascii", "ignore")
		except:
			raise Exception ("AppUtil.MeiRev.toJsonStr - Unexpected error:" +  str(sys.exc_info()[0]) + " in: " + self.title + " " + self.text)
			


	def __eq__(self, other):
		if self.appName == other.appName and self.title == other.title and self.text == other.text and self.date == other.date:
			return True
		else:	
			return False

	def __str__(self):
		return self.appName +": " + self.title
#######################################
##### End Classes #####################
#######################################

def ObjectToJsonStrList(objls):
	ret = []
	for el in objls:
		ret.append(el.toJsonStr())
	return ret

def MeiRevFromJsonFile(filename):
	ls = []
	lines = myUtility.ReadFileLines(filename)
	for l in lines:
		rev = MeiRev()
		rev.fromJson(l)
		ls.append(rev)
	return ls

def ReviewFromJsonFile(filename):
	ls = []
	lines = myUtility.ReadFileLines(filename)
	for l in lines:
		rev = Review()
		rev.fromJson(l)
		ls.append(rev)
	return ls

def ReviewFromItunesJsonFile(filename):
	ls = []
	lines = myUtility.ReadFileLines(filename)
	for l in lines:
		rev = Review()
		rev.fromItunesJson(l)
		ls.append(rev)
	return ls

def HistoryFromJsonFile(filename):
	ls = []
	lines = myUtility.ReadFileLines(filename)
	for l in lines:
		ent = HistoryEntry()
		ent.fromJson(l)
		ls.append(ent)
	return ls

def HistoryFromItunesFile(filename):
	ls = []
	lines = myUtility.ReadFileLines(filename)
	for l in lines:
		ent = HistoryEntry()
		ent.fromItunesJson(l)
		ls.append(ent)

def CreateEntryFromJson(json):
	ent = Entry("01")
	ent.fromJson(json)
	return ent

def EntryListFromJsonFile(filename):
	ls = []
	lines = myUtility.ReadFileLines(filename)
	for l in lines:
        	ent = CreateEntryFromJson(l)
		ls.append(ent)
	return ls

def SortByDate(listEntries):
	return sorted(listEntries, key=lambda entry: entry.lastRead)

def SortHistoryByDate(listEntries):
	return sorted(listEntries, key=lambda entry: entry.date, reverse=True)

def SortById(listEntries):
	return sorted(listEntries, key=lambda entry: entry.id)

def printList(listEntries):
	for entry in listEntries:
		print str(entry) + " "  + str(entry.lastRead)

