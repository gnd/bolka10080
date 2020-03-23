# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import argparse
import re
import unicodedata

# process user input
parser = argparse.ArgumentParser(description='Cleans a source file and saves data into an outfile.')
parser.add_argument('insubs', help='name of the original subtitle file')
parser.add_argument('intext', help='name of the replacement text file')
parser.add_argument('outsubs', help='name of the outfile')
args = parser.parse_args()

# read original subs into array
f = open(args.insubs, 'r')
subs = f.readlines()
f.close()

# read replacement text
f = open(args.intext, 'r')
newtext = f.read()
newtext = newtext.encode('utf8')
f.close()

# process subtitles
index = 1
time = ""
text = ""
submit = False
content = False
processed_subs = []
for sub in subs:
    if ((sub == '\r\n')):
        processed_subs.append([index, time, text])
        time = ""
        text = ""
        index += 1
        content = False
        continue
    if (sub.strip() == index):
        continue
    if ("-->" in sub):
        time = sub.strip()
        content = True
        continue
    if (content):
        text += sub.encode('utf8')

# replace text in subtitles with text of simillar length from newtext
index = 0
new_subs = []
for sub in processed_subs:
    text = sub[2]
    utterance = ""
    # construct a same length new utterance
    for i in range(len(text)):
        if (index + i >= len(newtext)):
            index = 0
        utterance += newtext[index + i]
    # if utterance a complete sentece or a word, move on
    if ((newtext[index + i] == '.') | (newtext[index + i] == ' ')):
        # add all together
        new_subs.append([sub[0], sub[1], utterance])
        index += i
        continue
    # otherwise find the end of the next word or sentence
    else:
        j = 1
        c = newtext[index + i]
        while ((c != '.') & (c != ' ')):
            if (index + i + j >= len(newtext)):
                index = 0
            utterance += newtext[index + i + j]
            c = newtext[index + i + j]
            j += 1
    # add all together
    new_subs.append([sub[0], sub[1], utterance])
    index += i + j

#print new_subs

# fush new subs to outfile
f = file(args.outsubs, 'w')
for sub in new_subs:
    f.write("%d\n" % sub[0])
    f.write(sub[1] + '\n')
    f.write(sub[2] + '\n\n')
f.close()
