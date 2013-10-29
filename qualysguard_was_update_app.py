#!/usr/bin/env python

'''Automate updating of multiple QualysGuard web apps.

Author: Parag Baxi <parag.baxi@gmail.com>
License: Apache License, Version 2.0
'''

'''To do:
Add ability to import CSV.
'''

import argparse
import base64, urllib2
import datetime, time
import logging
import os
import qualysapi
import random
import unicodedata

from collections import defaultdict
from texttable import Texttable

def list_apps(apps):
    """Print applications into a pretty table.
    """
    table = Texttable()
    table.set_cols_align(["r", "l", "l"])
    table.set_cols_valign(["m", "m", "m"])
    table.add_rows([ ['App #', 'App name', 'App ID #'], ], header = True) 
    c=0
    for webapp in apps:
        c+=1
        table.add_row([c, webapp['name'], webapp['id']])
    # Print table.
    print (table.draw() + '\n')
    return True

# Start of script.
# Declare the command line flags/options we want to allow.
parser = argparse.ArgumentParser(description = 'Automate updating of multiple QualysGuard webapps.')
parser.add_argument('-a', '--all_apps', action = 'store_true',
                    help = 'Select all web applications. Overwrites any tag filters.')
parser.add_argument('--config',
                    help = 'Configuration for Qualys connector.')
parser.add_argument('--debug', action = 'store_true',
                    help = 'Outputs additional information to log.')
parser.add_argument('-l', '--no_list', action = 'store_true', default = False,
                    help = 'Do not list all selected web applications. (Default = False)')
parser.add_argument('-t', '--tag',
                    help = 'Filter selection of web applications to those with TAG.')
#parser.add_argument('-T', '--Tags_file',
#                    help = 'Filter selection of web applications to those with all tags from TAGS_FILE (tags combined using a logical AND). Tags from file should be separated by line break.')
parser.add_argument('-u', '--update', default = 'post.xml',
                    help = 'Input XML file to POST update to webapps. (Default = post.xml)')
parser.add_argument('-x', '--no_update', action = 'store_true', default = False,
                    help = 'Do not update selected web applications. (Default = False)')
# Parse arguements.
c_args = parser.parse_args()
# Check requirements.
try:
    with open(c_args.update) as myfile:
        post = myfile.read().replace('\n', '')
except IOError:
    print 'No XML file found to update apps.'
    parser.print_help()
    exit(1)
# Create log directory.
PATH_LOG = 'log'
if not os.path.exists(PATH_LOG):
    os.makedirs(PATH_LOG)
# Set log options.
now = datetime.datetime.now()
BASE_FILENAME = '%s-%s' % (__file__,
                              datetime.datetime.now().strftime('%Y-%m-%d.%H-%M-%S'))
LOG_FILENAME = '%s/%s.log' % (PATH_LOG,
                              BASE_FILENAME)
# Set logging level.
if c_args.debug:
    # Enable debug level of logging.
    print "Logging level set to debug."
    logging.basicConfig(filename = LOG_FILENAME, format = '%(asctime)s %(message)s',
                        level = logging.DEBUG)
else:
    logging.basicConfig(filename = LOG_FILENAME, format = '%(asctime)s %(message)s',
                        level = logging.INFO)
# Validate arguments.
if not ((c_args.all_apps or c_args.tag or c_args.Tags_file)):
    parser.print_help()
    logging.error('Invalid run parameters.')
    exit(1)
# Configure Qualys API connector.
if c_args.config:
    qgc = qualysapi.connect(c_args.config)
else:
    qgc = qualysapi.connect()
# There may be more than 1000 apps so start with first possible record, # 0.
last_record = '0'
apps_to_update = []
print 'Downloading list of applications.'
while True:
    # Get list of web apps.
    query_uri = '/search/was/webapp'
    if c_args.all_apps:
        data = '''
        <ServiceRequest>
            <filters>
                <Criteria field="createdDate" operator="GREATER">2000-02-21T00:00:00Z</Criteria>
                <Criteria field="id" operator="GREATER">%s</Criteria>
            </filters>
            <preferences>
                <limitResults>1000</limitResults>
            </preferences>
        </ServiceRequest>''' % (last_record)
    elif c_args.tag:
        data = '''
        <ServiceRequest>
            <filters>
                <Criteria field="tags.name" operator="EQUALS">%s</Criteria>
                <Criteria field="id" operator="GREATER">%s</Criteria>
            </filters>
            <preferences>
                <limitResults>1000</limitResults>
            </preferences>
        </ServiceRequest>''' % (c_args.tag, last_record)
    search_apps = qgc.request(query_uri, data)
    # Parse list of web apps to associate each web app id with web app name.
    tree = objectify.fromstring(search_apps)
    for webapp in tree.data.WebApp:
        app = defaultdict(str)
        app_name = webapp.name.text
        # App name may be in unicode.
        if isinstance(app_name, unicode):
            # Decode to string.
            app_name = unicodedata.normalize('NFKD', app_name).encode('ascii','ignore')
        app['name'] = app_name
        app['id'] = webapp.id.text
        apps_to_update.append(app)
    if tree.hasMoreRecords.text == 'true':
        last_record = tree.lastId.text
    else:
        break
print '\n'
logging.info('apps_to_update = %s' % (apps_to_update))
if not c_args.no_list:
    list_apps(apps_to_update)
if c_args.no_update:
    print '\nNot updating the apps.\n'
    exit()
# Start updating.
apps_updated=[]
apps_not_updated=[]
for app in apps_to_update:
    logging.debug('Attempting to update %s, %s' % (app['name'], app['id']))
    # Limit updates to concurrency limit.
    # Update web app.
    query_uri = '/update/was/webapp/%s' % (app['id'])
    # Setup request to update web app.
    # Make request
    logging.info('Updating %s (web app ID %s)...' % (app['name'], app['id']))
    print 'Updating %s (web app ID %s)...' % (app['name'], app['id'])
    response = qgc.request(query_uri, post)
    print 'Done:'
    logging.info(response)
    print response
    app['response'] = response
    if '<errorMessage>' in app['response']:
        logging.warning('Could not update app %s, id %s.' % (str(app['name']), str(app['id'])))
        print 'Could not update app %s, id %s.\n' % (str(app['name']), str(app['id']))
        apps_not_updated.append(app)
    else:
        print 'Successfully updated app %s, id %s.\n' % (str(app['name']), str(app['id']))
        apps_updated.append(app)
# Write update status to file.
logging.debug('Writing results of initiating app updates to file.')
with open('%s-updated.txt' % (BASE_FILENAME), 'wb') as f:
    for app in apps_updated:
        f.write('%s, id %s, response: \n%s' % (str(app['name']), str(app['id']), str(app['response'])))
with open('%s-not_updated.txt' % (BASE_FILENAME), 'wb') as f:
    for app in apps_not_updated:
        f.write('%s, id %s, response: \n%s' % (str(app['name']), str(app['id']), str(app['response'])))
exit()