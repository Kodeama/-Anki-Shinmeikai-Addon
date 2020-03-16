# coding: utf8
import re, os
from aqt.qt import *
from anki.hooks import addHook
from aqt import mw

from shinmeikai_definitions import config
from codecs import open

source_directory = os.path.join(os.path.dirname(__file__),'data')
wordFreqListFileName = os.path.join(source_directory, config.Config().wordFreqList)
kanjiListFileName = os.path.join(source_directory, config.Config().kanjiList)

# for words not found
veryLargeFreq  = 999999
# for words in the frequency file, but without a frequency
emptyFrequency = 888888



def readDict(file, parseFun):
    # parseFun should a tuple, the first is the key, the second the value
    with open(file, encoding="utf-8") as f:
        lines = [parseFun(line) for line in f if "\t" in line]
    return dict(lines)

def readKeywords(file):

    def parse_line(line):
        f = line.rstrip().split("\t")[:2]
        assert len(f) == 2
        return (f[0], f[1])

    return readDict(file, parse_line)

def readFrequency(file):

    def parse_line(line):
        f = line.rstrip().split("\t")[:3]
        assert len(f) >= 2
        # if the second field does not exist, or
        # is not a valid number
        # simply set it to the largefreq
        try:
           freqInt = int(f[2])
        except:
            freqInt = emptyFrequency
        return ((f[0], f[1]), freqInt)

    return readDict(file, parse_line)


kanjiList = readKeywords(kanjiListFileName)

kanjiFreq = readFrequency(wordFreqListFileName)


def getRTKKeyword(str):
    kanji = filter (lambda a: a in kanjiList, list(str))
    # filter returns an iterator
    mappedKanji = map(lambda a: a + ": " + kanjiList.get(a, "this should never happen"), kanji)
    kanjiField = "</div><div>".join(mappedKanji)
    return "" if  (kanjiField == "") else ( "<div>" + kanjiField + "</div>")

def stringContainsKanji(searchTerm):
    for c in searchTerm:
        #Checks if codepoint of character is anything but hiragana/katakana
        if ord(c) < 12353 or ord(c) > 12543:
            return True
    return False

def getWordFrequency(strF, strK):

    if isinstance(strK, list):
        # iterate through each... find smallest
        listFreq = map(lambda k: kanjiFreq.get((k, strF), veryLargeFreq), strK)
        return min(listFreq)
    else:
        return kanjiFreq.get((strK, strF), veryLargeFreq)
