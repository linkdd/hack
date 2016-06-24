# -*- coding: utf-8 -*-

from riak import RiakClient
import json


c = RiakClient(nodes=[{
    'host': '127.0.0.1',
    'pb_port': '8087'
}])


nodes = c.bucket_type('nodes').bucket('default')
relationships = c.bucket_type('relationships').bucket('default')
graphs = c.bucket_type('graphs').bucket('default')


result = c.fulltext_search('relationships', 'type_set:X')

print(json.dumps(result, indent=4))
