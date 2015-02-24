import json
import sys
import myUtility
import datetime
import re

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

class Review:
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
		jsonStr = jsonStr + str(self.totalVote) + ",\"userLink\":\""
		jsonStr = jsonStr + self.userLink + "\",\"reviewId\":\""
		jsonStr = jsonStr + self.id + "\",\"country\":\""
		jsonStr = jsonStr + self.country + "\"}"
		return jsonStr.encode("ascii", "ignore")

	def remove_json_breakers(self, strn):
		ret = strn.replace("\n", " ")
		ret = ret.replace("\r", " ")
		ret = ret.replace("\r\n", " ")
		return ret

	def clean_text(self, strn):
		ret = strn.replace("\\", "\\\\")
		ret = ret.replace("\"", "\\\"")
		ret = re.sub('\\\*\"', '\\\"', ret) #This gets rid of extra parenthesis
		ret = ret.replace("\t", " ")
		ret = ret.replace("\r", " ")
		ret = ret.replace("\r\n", " ")
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
		except ValueError:
			print "Value error:", sys.exc_info()[0], " in: "
			print jsonStr
		except Exception as e:
			print e
			print "Unexpected error:", sys.exc_info()[0], " in: "
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
		except ValueError:
			print "Value error:", sys.exc_info()[0], " in: "
			print jsonStr
		except Exception as e:
			print e
			print "Unexpected error:", sys.exc_info()[0], " in: "
			print jsonStr
			


	def __str__(self):
		return self.id

	def Print(self):
		return self.text
		
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

