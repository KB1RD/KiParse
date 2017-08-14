#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 09:16:38 2017

@author: KB1RD
"""

import json
import argparse

import sys
import os

# ------------------------

version = "0.1"

# Allows for future implementations using classes or structures (or whatever
# their python equivalent is)
def dcreate():
    return []

# ------------------------

# n_catagories stores the number of catagories we currently have (so I don't
# have to look it up in a map)

n_catagories = 0
# Stores the filters
catagories = {None:["Misc"]}

# Stores the final output
sorted_pins = {None:dcreate()}

# ------------------------

# Argparse stuff
parser = argparse.ArgumentParser(description='KiParse Version '+str(version)+
            ' by KB1RD - Parse datasheets and create a CSV output for KiPart.\
            (https://xesscorp.github.io/KiPart)')

parser.add_argument("parser", help="Which parser to use? (As a path relative to\
    the install dir)")
parser.add_argument("json", help="The JSON object for parser configuration.")
parser.add_argument("catagory", help="A list of catagories to sort and name \
    pins. Each element in a catagory is seperated by a comma and the first one \
    becomes the catagory name.", nargs='+')

parser.add_argument("--no-file", "-n", help="Treats the JSON object as a JSON \
    string, not a JSON file", action='store_true')

parser.add_argument("--file", "-f", help="Set the output file")
parser.add_argument("--no-stdout", help="Don't print the output into stdout.\
    It's best to use this with --file.", action='store_true')

args = parser.parse_args()

# Make sure the parser can access this
global parser_settings
parser_settings = None
if args.no_file:
    try:
        parser_settings = json.loads(args.json)
    except: # This helps to sort out syntax errors from bash errors
        print "There's an error with the JSON. Here's what I see:", args.json
        sys.exit(-2)
else:
    with open(args.json, 'r') as json_file:
        parser_settings = json.load(json_file)

# Move the catagories in args into the catagory map
for catagory in args.catagory:
    catagories[n_catagories] = args.catagory[n_catagories].split(",")
    sorted_pins[n_catagories] = dcreate()
    n_catagories += 1

# ------------------------

# The raw output list from the parser (also must be global)

global pinList
pinList = []

# A couple utilities for the parser

def createPin(name, pin, type):
    return (name, str(pin), type)

# For accessing lists

def get_or_default(mp, i, default):
    try:
        return mp[i]
    except:
        return default

def get_or_fail(mp, i, msg):
    try:
        return mp[i]
    except:
        print msg
        sys.exit(1)

# Scripts should use the following variables:
# parser_settings - JSON Settings for the parser
# pinList         - A big list of unsorted pins

parser_path = args.parser

if not (parser_path.startswith('~') or parser_path.startswith('/') or 
    parser_path.startswith('.')):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    if not script_dir.endswith('/'):
        script_dir += '/'
    parser_path = script_dir+parser_path

if not '.' in args.parser.split('/')[-1]:
    execfile(args.parser+'.py')
else:
    execfile(args.parser)
    
# ------------------------

# Search the catagory lists and add the pins to the correct list

def findCatagory(line):
    for catagory in catagories:
        for catagory_search_term in catagories[catagory]:
            if catagory_search_term in line[0]:
                return catagory

# Now use that function

for line in pinList:
    catagory = findCatagory(line)
    sorted_pins[catagory].append(line)

# ------------------------

out_file = None
if not args.file is None:
    out_file = open(args.file, 'w')

# Splits the list into two parts (for right and left)

def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

def print_to_out(str):
    if not args.no_stdout:
        print str
    if not out_file is None:
        out_file.write(str+"\n")
    
def writeLine(line, side, catagory, catagory_suffix):
    side_name = "left"
    if side:
        side_name = "right"
    print_to_out(line[0]+", "+line[1]+", "+catagories[catagory][0]+
        str(catagory_suffix)+", "+line[2]+", "+side_name)

for catagory in sorted_pins:
    parts = []
    # Which unit to use. These appear like individual chips in the schematic
    chip = 0
    # Make sure the units have at most 50 pins
    while chip*50 < len(sorted_pins[catagory]):
        nextpos = (chip+1)*50
        if nextpos >= len(sorted_pins[catagory]):
            nextpos = len(sorted_pins[catagory])
        parts.append(sorted_pins[catagory][chip*50:nextpos])
        chip += 1
    
    index = 0
    for part in parts:
        partla, partlb = split_list(part)
        for parta in partla:
            writeLine(parta, False, catagory, index)
        for partb in partlb:
            writeLine(partb, True, catagory, index)
        index += 1

if not out_file is None:
    out_file.close()
