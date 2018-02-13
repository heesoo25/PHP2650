############################################################
##
## PHP 2650 Homework 1
##
## By Heesoo Kim and Melody Hsu
##
## Part 2: Funding and Publications
##
## Due Feb 17, 2018
##
############################################################

import csv
import urllib2
from urllib2 import urlopen

#############################################################
## Extract only research awards and its corresponding PI
## names from the NIH Harvard awards file.
## Save as 'NIHHarvard_extract.csv'
#############################################################

input_path = 'NIHHarvard.csv'
extract_path = 'NIHHarvard_extract.csv'

name_field = 'Contact PI / Project Leader'

with open(input_path, 'r') as in_file, open(extract_path, 'w') as out_file:
    csv_reader = csv.DictReader(in_file.read().splitlines())
    field_names = [name_field, 'Activity']
    csv_writer = csv.DictWriter(
        out_file,
        fieldnames=field_names,
        extrasaction='ignore')
    csv_writer.writeheader()
    for row in enumerate(csv_reader):
        csv_writer.writerow(row[1])
    print 'The research award and PI pairs have been extracted.'


#############################################################
## Clean the extracted data by getting rid of middle names
## and/or initials.
## Save as 'NIHHarvard_cleaned.csv'
#############################################################

cleaned_path = 'NIHHarvard_cleaned.csv'

with open (extract_path, 'r') as in_file, open(cleaned_path, 'w') as out_file:
    csv_reader = csv.DictReader(in_file.read().splitlines())
    field_names = csv_reader.fieldnames
    csv_writer = csv.DictWriter(out_file, field_names)
    csv_writer.writeheader()
    for row in enumerate(csv_reader):
        dic = row[1]
        names = dic[name_field].split()
        last_name_checker = True
        last_name = ''
        first_name = ''
        for n in names:
            if last_name_checker:
                if len(last_name) is 0:
                    last_name = n
                else:
                    last_name = last_name + ' ' + n
            else:
                first_name = n
                break
            if ',' in n:
                last_name = last_name[:len(last_name) - 1]
                last_name_checker = False

        dic['Contact PI / Project Leader'] = '%s, %s' % (last_name, first_name)
        csv_writer.writerow(dic)
    print 'The PI names have been cleaned.'


#############################################################
## Extract the number of publications of each PI from PubMed
## catalog.
## Save the extracted publications with corresponding PI as
## 'pi_publications.csv'
#############################################################

base_pubmed_url = 'https://www.ncbi.nlm.nih.gov/pubmed?term='
affiliation = '%20AND%20Harvard%5BAffiliation%5D'

pubs_path = 'pi_publications.csv'

with open(cleaned_path, 'r') as in_file, open(pubs_path, 'w') as out_file:

    csv_reader = csv.DictReader(in_file.read().splitlines())
    field_names = [name_field, 'Number of Publications']
    csv_writer = csv.DictWriter(out_file, field_names)
    csv_writer.writeheader()

    for row in enumerate(csv_reader):

        name = row[1][name_field]

        names = name.split()
        last_name_checker = True
        last_name = ''
        first_name = ''
        for n in names:
            if last_name_checker:
                if len(last_name) is 0:
                    last_name = n
                else:
                    last_name = last_name + '%20' + n
            else:
                first_name = n
                break
            if ',' in n:
                last_name = last_name[:len(last_name) - 1]
                last_name_checker = False

        name_search = last_name + '%2C%20' + first_name + '%5BAuthor%5D'
        pubmed_url = '%s(%s)%s' % (base_pubmed_url, name_search, affiliation)

        try:
            pubmed_html = urlopen(pubmed_url).read()

            start = pubmed_html.find('Items:')

            trim = pubmed_html[start:start + 25]
            stop = trim.find('<')
            trim = trim[:stop].split()
            if len(trim) == 0:
                num_publications = 1
            elif len(trim) == 2:
                num_publications = trim[1]
            else:
                num_publications = trim[5]
            print 'Number of publications successfully extracted for %s.' % name

        except:
            print 'Error: number of publications not extracted for %s.' % name
            num_publications = 'undefined'

        dic = {field_names[0]: name, field_names[1]: num_publications}
        csv_writer.writerow(dic)

    print 'The number of publications for each PI has been saved.'

