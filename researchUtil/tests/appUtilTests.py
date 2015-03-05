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
import unittest
import sys
import os
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import appUtil
import myUtility



class TextProcessingTests(unittest.TestCase):

	def setUp(self):
		self.rev = appUtil.Review()
		self.meiRev = appUtil.MeiRev()
		self.emojiList = myUtility.ReadFileLines("Emojilist.txt")

	def testReview_emojiDict(self):
		for el in self.emojiList:
			try:
				self.rev.replace_emojis(el)
			except:
				self.fail("Review.emojiDict - " + el + " is not in the emoji dictionary or failed to parse correctly")
		pass

	def testMeiReview_emojiDict(self):
		for el in self.emojiList:
			try:
				self.meiRev.replace_emojis(el)
			except:
				self.fail("Review.emojiDict - " + el + " is not in the emoji dictionary or failed to parse correctly")
		pass



if __name__ == '__main__':
	unittest.main()
