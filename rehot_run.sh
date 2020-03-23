#!/bin/bash
#
# run scrapy on rehot.sk
########################
# max 1078
scrapy crawl rehot_sk -a maxpages=1078 -a start_url=https://www.rehot.sk/ajax/1 -L ERROR

# output everything into rehot.in
python flush_jokes.py -d rehot.sk rehot.in
