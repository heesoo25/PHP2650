############################################################
##
## PHP 2650 Homework 1
##
## By Heesoo Kim and Melody Hsu
##
## Part 1: S & P 100 Stock Prices
##
## Due Feb 17, 2018
##
############################################################

import urllib2
import pprint
from urllib2 import urlopen
from bs4 import BeautifulSoup
import datetime
import time
import csv
import glob
import os

#############################################################
## Extract S&P symbols and company names from Wikipedia S&P
## 100 page
## Change the symbol BRK.B to BRK-B for Berkshire Hathaway
#############################################################

wiki_url = 'https://en.wikipedia.org/wiki/S%26P_100'
wiki_html = urlopen(wiki_url).read()
print 'Wikipedia S&P100 link loaded: ' + wiki_url


soup = BeautifulSoup(wiki_html,'html.parser')
tab = soup.findAll('table')[2]
print 'Stock info table found'

stock_array = []
for row in tab.findAll('tr'):
    stock = (col.text for col in row.findAll('td'))
    tstock = tuple(stock)
    if tstock == (u'BRK.B',u'Berkshire Hathaway'):
        tstock = (u'BRK-B',u'Berkshire Hathaway')
    if len(tstock) == 2:
        stock_array.append(tstock)

print 'Stock names saved.'

#############################################################
## Download historical stock prices from Yahoo in csv format.
## The date range here is from 01/01/2000 until today
#############################################################

# Handle HTTP redirect
class _MyHTTPREdirectHandler(urllib2.HTTPRedirectHandler):

    def http_error_302(self, req, fp, code, msg, headers):
        print 'Follow redirect...'
        return urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_302

# Initialize variables
yahoo_urls = []
csv_urls = []

# Check/make directory to save data
dir_path = os.getcwd()
if dir_path[-1] is not '/':
    dir_path = dir_path + '/'
unlabeled_directory = dir_path + 'unlabeled_stock_data'
if not os.path.exists(unlabeled_directory):
    os.makedirs(unlabeled_directory)
    print 'Unlabeled directory created.'

# Time range to get the historical data
start_date = datetime.datetime(2000, 1, 1, 0, 0)
start_date = str(int(time.mktime(start_date.timetuple())))
end_date = datetime.datetime.now()
end_date = end_date.strftime("%s")

# Make URLs simpler
base_yahoo = 'https://finance.yahoo.com/quote/'
filler_yahoo = '&interval=1d&filter=history&frequency=1d'
base_csv = 'https://query1.finance.yahoo.com/v7/finance/download/'

# Build Cookie processor
cookie_processor = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(_MyHTTPREdirectHandler, cookie_processor)
urllib2.install_opener(opener)

get_cookie = True

# Generate URLs and collect crumbs
for i in range(len(stock_array)):

    stock = stock_array[i][0]

    yahoo_url = '%s%s/history?period1=%s&period2=%s%s' % (
        base_yahoo, stock_array[i][0], start_date, end_date, filler_yahoo)
    yahoo_html = urlopen(yahoo_url).read()

    if get_cookie:
        # Collect Cookie
        cookie = str(cookie_processor.cookiejar)
        cookie = cookie[cookie.find("B="): cookie.find(" for")]

        print 'Cookies collected: ', cookie

        opener.addheaders.append(('Cookie', cookie))

        get_cookie = False

    crumb_loc = yahoo_html.find('CrumbStore')
    crumb = yahoo_html[crumb_loc:crumb_loc + 40]
    crumb_start = crumb.find(':"')
    crumb_end = crumb.find('"}')
    if crumb_end is -1:
        crumb = yahoo_html[crumb_loc:crumb_loc + 80]
        crumb_end = crumb.find('"}')
        assert crumb_end > 0
    crumb = crumb[crumb_start + 2:crumb_end]

    csv_url='%s%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s' % (
        base_csv, stock, start_date, end_date, crumb)

    yahoo_urls.append(yahoo_url)
    csv_urls.append(csv_url)

    print 'URLs for %s generated.' % stock_array[i][1]

    try:
        my_data = opener.open(csv_url).read()
        my_file = open(os.path.join(unlabeled_directory, '%s.csv' % stock), 'w')
        my_file.write(my_data)
        my_file.close()
        print 'Writing complete.'
    except:
        print 'Data was not saved for %s.' % stock_array[i][1]
        print 'URL attempted is: %s' % csv_url


#############################################################
## Add a column of the corresponding symbol for each csv file
## with the new column as the first column and comma
## separated from other columns.
## The new .csv file is saved as stockname_labeled.csv
#############################################################

# Check/make directory to save labeled data
labeled_directory = dir_path + 'labeled_stock_data'
if not os.path.exists(labeled_directory):
    os.makedirs(labeled_directory)
    print 'Labeled directory created.'

unlabeled_path = os.path.join(unlabeled_directory, '*.csv')

stock_name_start = len(unlabeled_directory)
if unlabeled_directory[-1] is not '/':
    stock_name_start += 1

for csv_file in glob.glob(unlabeled_path):

    input_file = str(csv_file)
    stock_name_end = input_file.find('.')
    stock_name = input_file[stock_name_start:stock_name_end]

    output_file = os.path.join(labeled_directory, '%s_labeled.csv' % stock_name)

    with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:
        csv_reader = csv.DictReader(in_file)
        field_names = ['Stock Symbol'] + csv_reader.fieldnames
        csv_writer = csv.DictWriter(out_file, field_names)
        csv_writer.writeheader()
        for row in enumerate(csv_reader):
            row[1]['Stock Symbol'] = stock_name
            csv_writer.writerow(row[1])

    print '%s data is labeled.' % stock_name


#############################################################
## Merge all of the .csv files in the folder into a single
## csv file.
## The new .csv file is saved as Merged.csv
#############################################################

labeled_path = os.path.join(labeled_directory, '*_labeled.csv')

# Merge files
merged_csv = open(os.path.join(dir_path, 'merged_stock_data.csv'), 'a')

read_header = True

for csv_file in glob.glob(labeled_path):

    if read_header:
        for line in open(csv_file):
            merged_csv.write(line)
        read_header = False

    file = open(csv_file)
    file.next()
    for line in file:
        merged_csv.write(line)
    file.close()

merged_csv.close()

print 'The .csv files have been merged.'
