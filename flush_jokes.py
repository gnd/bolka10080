# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import argparse
import ConfigParser

def clean(text):
    isok = True
    #if ('pozdravomVopred' in text): isok = False
    return isok

### load config
settings_file = 'bolka10080/settings_python'
config = ConfigParser.ConfigParser()
config.readfp(open(settings_file))
dbhost = config.get('database', 'DB_HOST')
dbuser = config.get('database', 'DB_USER')
dbpass = config.get('database', 'DB_PASS')
dbname = config.get('database', 'DB_NAME')
dbtable = config.get('database', 'DB_TABLE')
db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass, db=dbname)
cur = db.cursor()

# process user input
parser = argparse.ArgumentParser(description='Output scraped data from domain into outfile.')
parser.add_argument('-d', '--domain', default='all', help='the domain where the data was scraped from (default: all)')
parser.add_argument('-s', '--string', default='none', help='output only comments with STRING in text or nickname')
parser.add_argument('outfile', help='name of the outfile')
args = parser.parse_args()

# get all jokes from the db for a domain
jokes = []
if (args.domain == 'all'):
    if (args.string != 'none'):
        query = "SELECT joke FROM %s WHERE joke like '%%%s%%'" % (dbtable, args.string)
    else:
        query = "SELECT joke FROM %s" % (dbtable)
else:
    if (args.string != 'none'):
        query = "SELECT joke FROM %s WHERE domain = '%s'AND (joke like '%%%s%%')" % (dbtable, args.domain, args.string)
    else:
        query = "SELECT joke FROM %s WHERE domain = '%s'" % (dbtable, args.domain)
cur.execute(query)
if cur.rowcount == 0:
    sys.exit("Cant find jokes from %s" % domain)
else:
    for row in cur.fetchall():
        joke = str(row[0])
        jokes.append([joke])
db.close()

# print all the comments into a file
f = file(args.outfile, 'w')
for joke in jokes:
    if clean(joke[0]):
        f.write("\n\nZACIATOK VTIPU: %s\n" % (joke[0]))
f.close()
