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

emojiToEmoticon = { '\xf0\x9f\x99\x8b' : '(:',	#happy person raising one hand
	'\xF0\x9F\x98\x81': ':D',	#grinning face with smiling eyes
	'\xF0\x9F\x99\x8C': ':)',	#person raising both hands in celebration
	'\xF0\x9F\x98\x8C': '(^.^)',	#relieved face
	'\xF0\x9F\x98\x8A': '(^_^)',	#smiling face with smiling eyes
	'\xF0\x9F\x99\x8D' : '):',	#person frowning
	'\xF0\x9F\x99\x8E' : '):',	#person with pouting face
	'\xF0\x9F\x92\xA9' : '):',	#pile of poo
	'\xF0\x9F\x99\x86' : '*\\o/*',	#face with ok gesture
	'\xF0\x9F\x98\x87' : '0:)',	#smiling face with halo
	'\xF0\x9F\x98\x8E' : '8)',	#smiling face with sunglasses
	'\xF0\x9F\x98\xB1' : '8-0',	#face screaming in fear
	'\xF0\x9F\x99\x80' : '8-0',	#weary cat face
	'\xF0\x9F\x98\xAD' : ':\'(',	#loudly crying face
	'\xF0\x9F\x98\xBF' : ':\'(',	#crying cat face
	'\xF0\x9F\x98\xA2' : ':\'-(',	#crying face
	'\xF0\x9F\x98\x9E' : ':-(',	#disappointed face
	'\xF0\x9F\x98\x9A' : ':-*',	#kissing face with closed eyes
	'\xF0\x9F\x98\x97' : ':-*',	#kissing face
	'\xF0\x9F\x98\x99' : ':-*',	#kissing face with smiling eyes
	'\xF0\x9F\x98\xBD' : ':-*',	#kissing cat face with closed eyes
	'\xF0\x9F\x98\xA9' : ':-/',	#weary face
	'\xF0\x9F\x98\x82' : ':-D',	#face with tears of joy
	'\xF0\x9F\x98\xB9' : ':-D',	#cat face with tears of joy
	'\xF0\x9F\x98\xA8' : ':-O', 	#fearful face
	'\xF0\x9F\x98\x9B' : ':-P', 	#face with stuck-out tongue
	'\xF0\x9F\x98\x95' : ':-/',	#confused face - changed direction b/c parse errors
	'\xF0\x9F\x98\x81' : ':D',   	#grinning face with smiling eyes
	'\xF0\x9F\x98\x83' : ':D',  	#smiling face with open mouth
	'\xF0\x9F\x98\x80' : ':D',	#grinning face
	'\xF0\x9F\x98\xB8' : ':D',	#grinning cat face with smiling eyes
	'\xF0\x9F\x98\xBA' : ':D',	#smiling cat face with open mouth
	'\xF0\x9F\x98\xB7' : ':E',	#face with medical mask
	'\xF0\x9F\x98\xAE' : ':O',	#face with open mouth
	'\xF0\x9F\x98\xAF' : ':X',	#hushed face
	'\xF0\x9F\x98\x96' : ':[',	#confounded face
	'\xF0\x9F\x98\x90' : ':l',	#neutral face
	'\xF0\x9F\x98\x91' : ':|',	#expressionless face
	'\xF0\x9F\x98\xB6' : ':|',	#face without mouth
	'\xF0\x9F\x98\x89' : ';)',	#winking face
	'\xF0\x9F\x98\x8D' : '<3',	#smiling face with heart-shaped eyes
	'\xF0\x9F\x98\xBB' : '<3',	#smiling cat face with heart-shaped eyes
	'\xF0\x9F\x98\x9F' : '=[',	#worried face
	'\xF0\x9F\x98\xA0' : '>:(',	#angry face
	'\xF0\x9F\x98\xA1' : '>:(',	#pouting face
	'\xF0\x9F\x98\xBE' : '>:(',	#pouting cat face
	'\xF0\x9F\x98\x8F' : '>:)',	#smirking face
	'\xF0\x9F\x98\x88' : '>:)',	#smiling face with horns
	'\xF0\x9F\x98\xBC' : '>:)',	#cat face with wry smile
	'\xF0\x9F\x98\x86' : '>=D', 	#smiling face with open mouth and tightly-closed eyes
	'\xF0\x9F\x98\xA6' : 'D:', 	#frowning face with open mouth
	'\xF0\x9F\x98\xA7' : 'D:',	#anguished face
	'\xF0\x9F\x98\xAC' : 'D:',	#grimacing face
	'\xF0\x9F\x99\x85' : 'X(',	#face with no good gesture
	'\xF0\x9F\x98\xB2' : 'XO',	#astonished face
	'\xF0\x9F\x98\xB5' : 'XO',	#dizzy face
	'\xF0\x9F\x98\x9D' : 'XP',	#face with stuck-out tongue and tightly-closed eyes
	'\xF0\x9F\x98\x84' : '^_^',	#smiling face with open mouth and smiling eyes
	'\xF0\x9F\x98\x85' : '\'^_^',	#smiling face with open mouth and cold sweat
	'\xF0\x9F\x98\x8B' : ';P',	#face savouring delicious food
	'\xF0\x9F\x98\x9C' : ';P',	#face with stuck-out tongue and winking eye
	'\xF0\x9F\x98\x92' : '>_>',	#unamused face
	'\xF0\x9F\x98\xAA' : '-_-',	#sleepy face
	'\xF0\x9F\x98\xB4' : '-_-',	#sleeping face
	'\xF0\x9F\x98\x93' : '\'-_-',	#face with cold sweat
	'\xF0\x9F\x98\xA5' : '\'-_-', 	#disappointed but relieved face
	'\xF0\x9F\x98\xB0' : '\'-_-',	#face with open mouth and cold sweat
	'\xF0\x9F\x98\x98' : ';-*',	#face throwing a kiss
	'\xF0\x9F\x98\xA3' : '>_<',	#persevering face
	'\xF0\x9F\x98\xAB' : '>o<',	#tired face
	'\xF0\x9F\x98\xB3' : ':$',	#flushed face
	'\xF0\x9F\x99\x87' : ':$',	#person bowing deeply
	'\xF0\x9F\x98\x94' : ':(',	#pensive face
	'\xF0\x9F\x98\xA4' : '>:)',	#face with look of triumph
	'\xF0\x9F\x8C\x9F' : '~:)',	#glowing star
	'\xF0\x9F\x91\x8F' : '~:)',	#clapping hands sign
	'\xF0\x9F\x91\x8D' : '~:)',	#thumbs up sign
	'\xF0\x9F\x91\x8E' : '~:(',	#thumbs down sign
	'\xF0\x9F\x91\x8C' : '~:)',	#ok hand sign
	'\xF0\x9F\x91\x8A' : '~:|',	#fisted hand sign
	'\xF0\x9F\x91\xBF' : '>:(',	#imp
	'\xF0\x9F\x99\x88' : '~:|',	#see-no-evil monkey
	'\xF0\x9F\x99\x89' : '~:|',	#hear-no-evil monkey
	'\xF0\x9F\x99\x8A' : '~:|',	#speak-no-evil monkey
	'\xF0\x9F\x91\xB2' : ':D', 	#man with gua pi mao
	'\xF0\x9F\x91\xB3' : ':D', 	#man with turban
	'\xF0\x9F\x91\xAE' : ':D',	#police officer
	'\xF0\x9F\x91\xB7' : '-_-',	#construction worker
	'\xF0\x9F\x92\x82' : ':|',	#guardsman
	'\xF0\x9F\x91\xB6' : ':D',	#baby
	'\xF0\x9F\x91\xA6' : ':D',	#boy
	'\xF0\x9F\x91\xA7' : ':D',	#girl
	'\xF0\x9F\x91\xA8' : ':D',	#man
	'\xF0\x9F\x91\xA9' : ':D',	#woman
	'\xF0\x9F\x91\xB4' : ':D',	#older man
	'\xF0\x9F\x91\xB5' : ':)',	#older woman
	'\xF0\x9F\x91\xB1' : ':D',	#person with blond hair
	'\xF0\x9F\x91\xBC' : ':D',	#baby angel
	'\xF0\x9F\x91\xB8' : ':)',	#princess
	'\xF0\x9F\x92\x80' : '~:(',	#skull
	'\xF0\x9F\x91\xBD' : ':)',	#extraterrestrial alien
	'\xF0\x9F\x94\xA5' : '~:|',	#fire
	'\xF0\x9F\x92\xAB' : '~:)',	#dizzy
	'\xF0\x9F\x92\xA5' : '~:|',	#boom symbol	
	'\xF0\x9F\x92\xA2' : '~:(',	#anger symbol	
	'\xF0\x9F\x92\x8F' : '<3',	#kiss
	'\xF0\x9F\x92\x91' : '<3',	#couple with heart
	'\xF0\x9F\x91\xB0' : ':D',	#bride with veil	
	'\xF0\x9F\x92\x9B' : '<3',	#yellow heart
	'\xF0\x9F\x92\x99' : '<3',	#blue heart
	'\xF0\x9F\x92\x9C' : '<3',	#purple heart
	'\xF0\x9F\x92\x9A' : '<3',	#green heart
	'\xF0\x9F\x92\x94' : '</3',	#broken heart
	'\xF0\x9F\x92\x97' : '<3',	#growing heart
	'\xF0\x9F\x92\x93' : '<3',	#beating heart
	'\xF0\x9F\x92\x95' : '<3 <3',	#two hearts
	'\xF0\x9F\x92\x96' : '<3',	#sparkling heart
	'\xF0\x9F\x92\x9E' : '<3 <3',	#revolving hearts
	'\xF0\x9F\x92\x98' : '<3',	#heart with arrow
	'\xF0\x9F\x92\x8C' : '<3',	#love letter
	'\xF0\x9F\x92\x8B' : ':-*'	#kiss mark
	}
