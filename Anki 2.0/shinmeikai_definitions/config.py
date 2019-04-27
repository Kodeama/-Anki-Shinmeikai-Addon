#!/usr/bin/python
# coding: utf8
class Config(object):
    enableKanjiKeywords = True
    addFuriganaToDef = True
    maxNumberOfDefs = 3
    orderDefByFreq = True
    defSrcField = ["Focus"]
    defDstField = ["Meaning"]
    kanjiSrcField = ["Focus"]
    kanjiDstField = ["Kanji"]

    wordFreqList = "10kData.txt"
    kanjiList = "HeisigKeywords.txt"
