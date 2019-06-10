#!/usr/bin/python
# coding: utf8
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
import importlib

from anki.hooks import addHook

from shinmeikai_definitions import config, shinmeikai, jpParser

conf = config.Config()

# Importing mecab from Japanese Support or MIA Japanese Support
try:
    reading = importlib.import_module('MIAJapaneseSupport.reading')
    mecab = reading.MecabController()
except: # If MIA Japanese Support Plugin is not Installed
    reading = importlib.import_module(conf.japaneseSupportPluginFolderName+'.reading')
    mecab = reading.mecab

mecab.setup()

#ANKI SPECIFIC
def generateDefinitions(selectedNotes):
    global mecab
    mw.checkpoint("Shinmeikai Definitions")
    mw.progress.start()
    for currentSelectedNote in selectedNotes:
        note = mw.col.getNote(currentSelectedNote)

        if conf.enableKanjiKeywords:
            rtkKeywords = None
            for field in conf.kanjiSrcField:
                if field in note:
                    srcTxt = mw.col.media.strip(note[field])
                    if jpParser.stringContainsKanji(srcTxt):
                        rtkKeywords = jpParser.getRTKKeyword(srcTxt)
            if rtkKeywords != None:
                for field in conf.kanjiDstField:
                    if field in note:
                        if not note[field]:
                            note[field] = rtkKeywords

        src = None
        for field in conf.defSrcField:
            if field in note:
                src = field
                break
        if not src:
            continue

        dst = None
        for field in conf.defDstField:#dstFields:
            if field in note:
                dst = field
                break
        if not dst:
            continue

        # already contains data, skip
        if note[dst]:
            continue

        srcTxt = mw.col.media.strip(note[src])
        if not srcTxt.strip():
            continue

        try:
            definition = getCompleteDefinitionsForWord(srcTxt)
            #definition.decode('unicode-escape')
            #definition.encode('utf-8')
            #encodedDef = definition.encode('utf8')
            '''
            temp
            '''
            #note[dst] = shinmeikai.getDefsOfWord(srcTxt, conf)
            note[dst] = definition
            #note[dst] = shinmeikai.testEncodingFunction()


            #note[dst] = srcTxt#mecab.reading(srcTxt)
        except Exception as e:
            mecab = None
            raise
        note.flush()
    mw.progress.finish()
    mw.reset()

def setupMenu(browser):
    action = QAction("Bulk Add Shinmeikai Definitions", browser)
    action.triggered.connect(lambda: generateDefinitions(browser.selectedNotes()))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(action)

addHook("browser.setupMenus", setupMenu)

#NON ANKI SPECIFIC
def getCompleteDefinitionsForWord(targetWord):
    defs = shinmeikai.getDefsOfWord(targetWord, conf)
    sortedDefs = sortDefinitions(defs)
    optimallySelectedDefs = removeOverflowDefinitions(sortedDefs)
    formatedDef = defListToString(optimallySelectedDefs)
    if formatedDef == None:
        return "";
    if conf.addFuriganaToDef:
        formatedDef = mecab.reading(formatedDef)
    completeDefinitions = correctSpacing(formatedDef)
    return completeDefinitions

def sortDefinitions(defList):
    #print(defList)
    sortedSubDefList = sorted(defList, key=lambda y : y[1])
    return sortedSubDefList

def removeOverflowDefinitions(defList):
    numOfDefs = len(defList)
    desiredNumOfDef = conf.maxNumberOfDefs
    if numOfDefs > desiredNumOfDef:
            for x in range(0, numOfDefs - desiredNumOfDef):
                del defList[-1] #Remove last element
    return defList

def defListToString(defList):
    formatedDef = ""
    for x in defList:
        formatedDef += x[0] + "<div></div>"
    return formatedDef.replace(r"[", "TEMPSPACING") #Prevent pitch accent to not display as furigana

def correctSpacing(definition):
    returnDef = definition.replace("\\n", "<div></div>")
    returnDef = returnDef.replace("\\ n", "<div></div>")
    returnDef = returnDef.replace("TEMPSPACING", " [")
    returnDef = returnDef.replace("[ ", "[")
    return returnDef

###TESTS
def test():
    defs = shinmeikai.getDefsOfWord(sys.argv[1], conf)
    #print(defs)
    sortedDefs = sortDefinitions(defs)
    #print(sortedDefs)
    optimallySelectedDefs = removeOverflowDefinitions(sortedDefs)
    #print(optimallySelectedDefs)
    formatedDef = defListToString(optimallySelectedDefs)
    #print(formatedDef)
    if conf.addFuriganaToDef:
        formatedDef = mecab.reading(formatedDef)
    #print(formatedDef)
    return formatedDef
    #print("Searching for...\nKanji: "+sys.argv[2]+".\nHira: "+sys.argv[1]+".")
    #print(jpParser.getWordFreq(sys.argv[1], sys.argv[2]))
#test()
