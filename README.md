qualysguard_was_update_app
==========================

Automate updating of multiple QualysGuard web apps.

Workflow
========

Here's what the script does:

1. Selects the applications you want to scan based on filters.
2. Lists selected applications.
3. Runs update against applications.

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
