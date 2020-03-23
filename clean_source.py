# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import argparse
import re
import unicodedata

def clean_text(text):
    text = text.replace('\t','')                                        # remove useless tabs
    text = text.replace('<br>',' ').replace('\n',' ').replace('\r',' ') # remove linebreaks
    text = re.sub('\.+','.', text)                                      # many dots > one dot
    text = re.sub('\!+','!', text)                                      # many ! > one !
    text = re.sub('\?+','?', text)                                      # many ? > one ?
    text = re.sub('\,+',',', text)                                      # many , > one ,
    text = re.sub('\*+','*', text)                                      # many * > one *
    # remove dashes
    text = text.replace(' - ','')                                       # remove dashes
    # remove all links
    text = re.sub('<[^<]+?>', '', text)                                 # Remove HTML tags
    text = re.sub('http.*?( |$)',', ', text)                            # Remove http - starting addresses
    text = re.sub('www.*?( |$)',', ', text)                             # Remove www - starting addresses
    text = re.sub('[a-zA-Z]*\.(.*)\.php(\?)?.*?( |$)','', text)         # Remove .php containing links
    text = re.sub('[a-zA-Z]*\.(.*)\.html(\?)?.*?( |$)','', text)        # Remove .php containing links
    # dots
    text = re.sub('([a-zA-Z]?)\.([a-zA-Z]+)', "\\1. \\2", text)         # Fix . at end of sentence
    text = text.replace('.  ','. ')
    text = text.replace(' .','. ')
    # exclamatio marks
    text = re.sub('([a-zA-Z]?)\!([a-zA-Z]+)', "\\1! \\2", text)         # Fix ! at end of sentence
    text = text.replace('!  ','! ')
    text = text.replace(' !','! ')
    # question marks
    text = re.sub('([a-zA-Z]?)\?([a-zA-Z]+)', "\\1? \\2", text)         # Fix ? at end of sentence
    text = text.replace('?  ','? ')
    text = text.replace(' ?','? ')
    # commas
    text = re.sub('([a-zA-Z]?)\,([a-zA-Z]+)', "\\1, \\2", text)         # Fix , at end of sentence
    text = text.replace(',  ',', ')
    text = text.replace(' ,',', ')
    # spaces
    text = re.sub('\ +',' ', text)                                      # many ' ' > one ' '
    # remove various bordel
    text = text.replace('"','')                                         # remove double quotes
    text = text.replace("'",'')                                         # remove single quotes
    # remove initial space
    if text[0] == ' ':
        text = text[1:]
    return text

def simple_clean_text(text):
    text = text.replace('<br>',' ').replace('\n',' ').replace('\r',' ') # remove linebreaks
    text = re.sub('\.+','.', text)                                      # many dots > one dot
    text = re.sub('\!+','!', text)                                      # many ! > one !
    text = re.sub('\?+','?', text)                                      # many ? > one ?
    text = re.sub('\,+',',', text)                                      # many , > one ,
    text = re.sub('\*+','*', text)                                      # many * > one *
    text = re.sub('\ +',' ', text)                                      # many ' ' > one ' '
    # remove various bordel
    text = text.replace('"','')                                         # remove double quotes
    text = text.replace("'",'')                                         # remove single quotes
    text = re.sub('<[^<]+?>', '', text)                                 # Remove HTML tags
    text = re.sub('http.*? ',', ', text)                               # Remove http - starting addresses
    text = re.sub('www.*? ',', ', text)                                # Remove www - starting addresses
    return text

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

# process user input
parser = argparse.ArgumentParser(description='Cleans a source file and saves data into an outfile.')
parser.add_argument('infile', help='name of the infile')
parser.add_argument('outfile', help='name of the outfile')
args = parser.parse_args()

# read file into array
f = open(args.infile, 'r')
lines = f.readlines()
f.close()

# construct a clean one line out of infile
oneline = ""
for line in lines:
    output = line.encode('utf8')
    output = strip_accents(output)
    output = clean_text(output)
    oneline += ' ' + output

# output to file
f = open(args.outfile, 'w')
f.write(oneline)
f.close()
