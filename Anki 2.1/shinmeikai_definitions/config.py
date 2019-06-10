#!/usr/bin/python
# coding: utf8
class Config(object):
    enableKanjiKeywords = True
    addFuriganaToDef = True
    orderDefByFreq = True
    maxNumberOfDefs = 3
    defSrcField = ["Focus"]
    defDstField = ["Meaning"]
    kanjiSrcField = ["Focus"]
    kanjiDstField = ["Kanji"]

    wordFreqList = "10kData.txt"
    kanjiList = "HeisigKeywords.txt"
    japaneseSupportPluginFolderName="3918629684"
