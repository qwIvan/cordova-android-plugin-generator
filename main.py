#!/usr/bin/env python3
from lxml import etree
import sys, glob, os
cordova_path = sys.argv[1]
android_basedir = 'android'
plugin_xml_path = 'plugin.xml'
os.chdir(cordova_path)
if os.path.isfile(plugin_xml_path):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(plugin_xml_path,parser)
else:
    tree = etree.ElementTree()
root = tree.getroot()
for platform in root.findall('platform'):
    if platform.get('name')=='android':
        android = platform
        for resource_file in android.findall('resource-file'):
            android.remove(resource_file)
        os.chdir(android_basedir)
        for filepath in glob.iglob('**', recursive=True):
            if os.path.isfile(filepath):
                resource_file = etree.Element('resource-file')
                resource_file.set('src',os.path.join(android_basedir,filepath))
                resource_file.set('target',os.path.join(filepath))
                android.append(resource_file)
        os.chdir(os.path.pardir)
        tree.write(plugin_xml_path,pretty_print=True)
