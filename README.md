qualysguard_was_update_app
==========================

Automate updating of multiple QualysGuard web apps.

Workflow
========

Here's what the script does:

1. Selects the applications you want to scan based on filters.
2. Lists selected applications.
3. Runs update against applications.

Usage
=====

    usage: qualysguard_was_update_app.py [-h] [-a] [--config CONFIG] [--debug]
                                     [-l] [-t TAG] [-u UPDATE] [-x]

    Automate updating of multiple QualysGuard webapps.
    
    optional arguments:
      -h, --help            show this help message and exit
      -a, --all_apps        Select all web applications. Overwrites any tag
                            filters.
      --config CONFIG       Configuration for Qualys connector.
      --debug               Outputs additional information to log.
      -l, --no_list         Do not list all selected web applications. (Default =
                            False)
      -t TAG, --tag TAG     Filter selection of web applications to those with
                            TAG.
      -u UPDATE, --update UPDATE
                            Input XML file to POST update to webapps. (Default =
                            post.xml)
      -x, --no_update       Do not update selected web applications. (Default =
                            False)

Examples
========
List web applications with tag "Product Management".

    python qualysguard_scan_queue.py --tag "Product Management" --no_update

Update all web applications.

    python qualysguard_scan_queue.py --all_apps

Update web applications with tag "QA" from XML file 'mypost.xml'

    python qualysguard_scan_queue.py --tag "QA" --update "mypost.xml"

Troubleshoot why script will not work (put in debug mode)

    python qualysguard_scan_queue.py --all_apps --debug

Sample output
=============
Goal: Update all webapps tagged with "PB - WAS static" with a blacklist.

Input XML file, post.xml:

    <ServiceRequest>
      <data>
        <WebApp>
          <urlBlacklist>
            <set>
              <UrlEntry regex="true"><![CDATA[http://rg.blacklist.*.com]]></UrlEntry>
            </set>
          </urlBlacklist>
        </WebApp>
      </data>
    </ServiceRequest>

Script run:

    $ python qualysguard_was_update_app.py -t "PB - WAS static"
    Downloading list of applications.
    
    
    +-------+---------------------+----------+
    | App # |      App name       | App ID # |
    +=======+=====================+==========+
    |     1 | Gruyere-Application | 24115    |
    +-------+---------------------+----------+
    |     2 | Gruyere             | 160847   |
    +-------+---------------------+----------+
    |     3 | My Personal BodgeIt | 12717134 |
    +-------+---------------------+----------+
    
    Updating Gruyere-Application (web app ID 24115)...
    Done:
    <?xml version="1.0" encoding="UTF-8"?>
    <ServiceResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://qualysapi.qualys.com/qps/xsd/3.0/was/webapp.xsd">
      <responseCode>SUCCESS</responseCode>
      <count>1</count>
      <data>
        <WebApp>
          <id>24115</id>
        </WebApp>
      </data>
    </ServiceResponse>
    
    Successfully updated app Gruyere-Application, id 24115.
    
    Updating Gruyere (web app ID 160847)...
    Done:
    <?xml version="1.0" encoding="UTF-8"?>
    <ServiceResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://qualysapi.qualys.com/qps/xsd/3.0/was/webapp.xsd">
      <responseCode>SUCCESS</responseCode>
      <count>1</count>
      <data>
        <WebApp>
          <id>160847</id>
        </WebApp>
      </data>
    </ServiceResponse>
    
    Successfully updated app Gruyere, id 160847.
    
    Updating My Personal BodgeIt (web app ID 12717134)...
    Done:
    <?xml version="1.0" encoding="UTF-8"?>
    <ServiceResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://qualysapi.qualys.com/qps/xsd/3.0/was/webapp.xsd">
      <responseCode>SUCCESS</responseCode>
      <count>1</count>
      <data>
        <WebApp>
          <id>12717134</id>
        </WebApp>
      </data>
    </ServiceResponse>
    
    Successfully updated app My Personal BodgeIt, id 12717134.

Requirements
============

1. Python 2.6+
2. qualysapi
3. texttable

How to install libraries
------------------------

Install pip:

    curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python

Install libraries:

    pip install qualysapi Texttable
