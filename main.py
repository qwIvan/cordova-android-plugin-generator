#!/usr/bin/env python3
'''
generator cordova android plugin
'''
import sys
import glob
import os
from lxml import etree
CORDOVA_PATH = sys.argv[1]
ANDROID_BASEDIR = 'android'
PLUGIN_XML_PATH = 'plugin.xml'
os.chdir(CORDOVA_PATH)
if os.path.isfile(PLUGIN_XML_PATH):
    PARSER = etree.XMLParser(remove_blank_text=True)
    TREE = etree.parse(PLUGIN_XML_PATH, PARSER)
else:
    TREE = etree.ElementTree()
ROOT = TREE.getroot()
for platform in ROOT.findall('platform'):
    if platform.get('name') == 'android':
        android = platform
        for resource_file in android.findall('resource-file'):
            android.remove(resource_file)
        os.chdir(ANDROID_BASEDIR)
        for filepath in glob.iglob('**', recursive=True):
            if os.path.isfile(filepath):
                resource_file = etree.Element('resource-file')
                resource_file.set(
                    'src', os.path.join(ANDROID_BASEDIR, filepath))
                resource_file.set('target', os.path.join(filepath))
                android.append(resource_file)
        os.chdir(os.path.pardir)
        TREE.write(PLUGIN_XML_PATH, pretty_print=True)
