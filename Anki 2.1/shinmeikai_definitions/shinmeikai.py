# coding: utf8
import re, os
from . import jpParser
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

#parserObj = parser.Parser()
source_directory = os.path.join(os.path.dirname(__file__),'data')

dictFileNamePrefix = os.path.join(source_directory, "Shinmeikai", "shinmeikai_")

amountOfDictionaryFiles = 9

def getDefsOfWord(word, conf):
    #return u"私はバカです"
    return searchForWordInShinmeikai(word, conf)

def searchForWordInShinmeikai(searchTerm, conf):
    dictionaryCounter = 1
    defArray = []
    definitionFound = False
    rtkKeywordList = []

    if jpParser.stringContainsKanji(searchTerm):
        regex = "(\[\""+searchTerm+"\"(,.*?){7}\])" #With kanji
    else:
        regex = "(\[\".{0,8}\",\""+searchTerm+"\"(,.*?){6}\])" #Without kanji

    #Looks for matches in all shinmeikai dictionary files.
    while True:
        dict = open(dictFileNamePrefix +str(dictionaryCounter)+".txt", "rb")
        contents = dict.read().decode("UTF-8")
        dict.close()

        pattern = re.compile(regex, re.UNICODE)
        export = pattern.findall(contents)
        #return pattern.pattern
        #return str(export).decode('unicode-escape')
        if len(export) >= 1:
            definitionFound = True
            for x in export:
                #after = x
                #after.encode("UTF-8")
                #return str(x).decode('unicode-escape')
				########### innerDef = extractDefFromElement(str(x).decode('unicode-escape'))
                innerDef = extractDefFromElement(str(x))
                hira = extractHiraFromElement(innerDef)
                kanji = extractKanjiFromElement(innerDef)

                if kanji == None:#If word doesnt have kanji, search with hira for both fields
                    kanji = hira
                freq = jpParser.getWordFreq(hira, kanji)

                defArray.append((innerDef, int(freq)))
        if dictionaryCounter >= amountOfDictionaryFiles:
            if definitionFound == False:
                defArray = ""
            break
        dictionaryCounter += 1
    return (defArray)

def extractDefFromElement(org):
    regex = "(.*)\[.*\[\"(.*?)\"\]"
    matchObj = re.match(regex, org)
    if matchObj == None:
        returnValue = None
    else:
        returnValue = matchObj.group(2)
        returnValue = re.sub(r'\\\\', r'\\', returnValue)
    return returnValue

def extractHiraFromElement(org):
    regex = "(.*?) "
    matchObj = re.match(regex, org)
    if matchObj == None:
        returnValue = None
    else:
        returnValue = matchObj.group(1)
    return returnValue


def extractKanjiFromElement(org):
    regex = ".*?【(.*?)】"
    matchObj = re.match(regex, org)
    if matchObj == None:
        return None
    else:
        returnValue = matchObj.group(1)

    #If more than one kanji, ex(内・家) for うち
    #return an array of kanji, It seems like the "・" character doesnt work with regex?
    #Currently only handles two different words, like うち -> 家 and 内 works
    matchObj = re.search("・", returnValue)
    if matchObj != None: #Multiple kanji found
        matchObj = re.match("(.*?)・(.*?) ", returnValue+" ")
        if matchObj != None:
            returnValue = []
            returnValue.append(matchObj.group(1))
            returnValue.append(matchObj.group(2))
    return returnValue
