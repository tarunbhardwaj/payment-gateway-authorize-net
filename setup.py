#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

    Payment Gateway Setup

    :copyright: (c) 2013-2014 by Openlabs Technologies & Consulting (P) Ltd.
    :license: BSD, see LICENSE for more details

'''
import sys
import re
import os
import unittest
import ConfigParser
from setuptools import setup, Command


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class SQLiteTest(Command):
    """
    Run the tests on SQLite
    """
    description = "Run tests on SQLite"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from trytond.config import CONFIG
        CONFIG['db_type'] = 'sqlite'
        os.environ['DB_NAME'] = ':memory:'

        from tests import suite
        test_result = unittest.TextTestRunner(verbosity=3).run(suite())

        if test_result.wasSuccessful():
            sys.exit(0)
        sys.exit(-1)


config = ConfigParser.ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
major_version, minor_version, _ = info.get('version', '0.0.1').split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

requires = [
    'py-authorize',
]

MODULE = 'payment_gateway_authorize_net'
PREFIX = 'openlabs'
MODULE2PREFIX = {
    'payment_gateway': 'openlabs',
}

for dep in info.get('depends', []):
    if not re.match(r'(ir|res|webdav)(\W|$)', dep):
        requires.append(
            '%s_%s >= %s.%s, < %s.%s' % (
                MODULE2PREFIX.get(dep, 'trytond'), dep,
                major_version, minor_version, major_version, minor_version + 1
            )
        )
requires.append(
    'trytond >= %s.%s, < %s.%s' % (
        major_version, minor_version, major_version, minor_version + 1
    )
)
setup(
    name='%s_%s' % (PREFIX, MODULE),
    version=info.get('version', '0.0.1'),
    description="Tryton module for Payment Gatway/Merchant Integration",
    author="Openlabs Technologies & consulting (P) Limited",
    author_email='info@openlabs.co.in',
    url='http://www.openlabs.co.in',
    package_dir={'trytond.modules.%s' % MODULE: '.'},
    packages=[
        'trytond.modules.%s' % MODULE,
        'trytond.modules.%s.tests' % MODULE,
    ],
    package_data={
        'trytond.modules.%s' % MODULE: info.get('xml', [])
        + info.get('translation', [])
        + ['tryton.cfg', 'locale/*.po', 'tests/*.rst', '*.odt']
        + ['view/*.xml'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Tryton',
        'Topic :: Office/Business',
    ],
    license='GPL-3',
    install_requires=requires,
    extras_require={
        'docs': ['sphinx', 'sphinx_rtd_theme'],
    },
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    %s = trytond.modules.%s
    """ % (MODULE, MODULE),
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    cmdclass={
        'test': SQLiteTest,
    },
)
