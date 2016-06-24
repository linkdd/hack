#!/usr/bin/env python
# -*- coding:utf-8 -*-

from riak import RiakClient
import traceback
import sys


try:
    c = RiakClient(nodes=[{
        'host': '127.0.0.1',
        'pb_port': '8087'
    }])

    with open('node.xml') as f:
        print('-- Create search schema: nodes')
        c.create_search_schema('nodes', f.read())

    with open('relationship.xml') as f:
        print('-- Create search schema: relationships')
        c.create_search_schema('relationships', f.read())

    with open('graph.xml') as f:
        print('-- Create search schema: graphs')
        c.create_search_schema('graphs', f.read())

    print('-- Create search index: nodes')
    c.create_search_index('nodes', 'nodes')
    print('-- Create search index: relationships')
    c.create_search_index('relationships', 'relationships')
    print('-- Create search index: graphs')
    c.create_search_index('graphs', 'graphs')

except Exception:
    traceback.print_exc()
    sys.exit(1)
