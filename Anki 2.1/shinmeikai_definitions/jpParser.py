# coding: utf8
import re, os
from aqt.qt import *
from anki.hooks import addHook
from aqt import mw

from shinmeikai_definitions import config
from codecs import open

source_directory = os.path.join(os.path.dirname(__file__),'data\\')

dict = open(source_directory+config.Config().wordFreqList, "rb")
contents = dict.read().decode("UTF-8")
dict.close()

dict = open(source_directory+config.Config().kanjiList, "rb")
kanjiList = dict.read().decode("UTF-8")
dict.close()

def stringContainsKanji(searchTerm):
    for c in searchTerm:
        #Checks if codepoint of character is anything but hiragana/katakana
        if ord(c) < 12353 or ord(c) > 12543:
            return True
    return False

def getWordFreq(hira, kanji):
    matchObj = None
    freq = 999999
    if isinstance(kanji, list):
        for k in kanji:
            regex = ""+k+"	"+hira+"	(.*?)	"
            matchObj = re.search(regex, contents)
            if matchObj != None and int(matchObj.group(1)) < freq:
                freq = matchObj.group(1)

    else:
        regex = ""+kanji+"	"+hira+"	(.*?)	"
        matchObj = re.search(regex, contents)
        if matchObj != None:
            freq = re.search(regex, contents).group(1)

    #if matchObj == None:
    #    return 999999 #Just something high so the sort gets this word to the back of the list

    return freq

def getRTKKeyword(kanji):
    kanjiFound = False
    kanjiField = ""
    keywordList = []
    #print("recieved kanji len: "+ str(len(kanji)))
    for x in range(0, len(kanji)):
        #print(str(x))
        if stringContainsKanji(kanji[x]):
            #print("Contained kanji")
            regex = kanji[x]+"\t(.*)"
            keyword = re.search(regex, kanjiList)
            #print("Keywords: "+str(keyword))
            if keyword != None:
                if kanjiFound:
                    kanjiField += "<div></div>"
                kanjiField += ""+kanji[x]
                kanjiField += " "+str(keyword.group(1)).replace("\r","")
                kanjiFound = True
                #print("Found kanji: "+kanji[x]+" = "+keyword.group(1))
    #print(kanjiField)
    return kanjiField
