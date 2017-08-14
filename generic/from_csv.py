# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 14:47:05 2017

@author: KB1RD
"""

import csv

with open(parser_settings['file'], 'rb') as csvfile:
    
    delim = get_or_default(parser_settings, 'delim', ',')
    nl_delim = get_or_default(parser_settings, 'nl_delim', '\n')
    
    i_name = int(get_or_fail(parser_settings, 'name', 'Failed to read name \
index. Be sure to specify "name" in your JSON'))
    i_pin  = int(get_or_fail(parser_settings, 'pin', 'Failed to read pin \
index. Be sure to specify "pin" in your JSON'))
    i_type = int(get_or_fail(parser_settings, 'type', 'Failed to read type \
index. Be sure to specify "type" in your JSON'))
    
    reader = csv.reader(csvfile, delimiter=delim.encode('ascii', 'ignore'), 
        lineterminator=nl_delim.encode('ascii', 'ignore'))
    
    pinList = []
    
    for row in reader:
        pinList.append(createPin(row[i_name], row[i_pin], row[i_type]))
