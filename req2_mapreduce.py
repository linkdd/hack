# -*- coding: utf-8 -*-

from link.middleware.core import Middleware
from b3j0f.task import register

from riak import RiakClient
import random
import json


c = RiakClient(nodes=[{
    'host': '127.0.0.1',
    'pb_port': '8087'
}])


nodes = c.bucket_type('nodes').bucket('default')
relationships = c.bucket_type('relationships').bucket('default')
graphs = c.bucket_type('graphs').bucket('default')


@register('map-forward')
def map_forward(mapper, node):
    targets = node.get('targets_set', [])

    if not isinstance(targets, list):
        targets = [targets]

    for target in targets:
        _, node_id = target.split(':')
        mapper.emit('forward', node_id)


@register('reduce-forward')
def reduce_forward(reducer, key, node_ids):
    objs = nodes.multiget(node_ids)
    docs = []

    for obj in objs:
        doc = {
            '_yz_rt': 'nodes',
            '_yz_rb': 'default',
            '_yz_rk': obj.key,
            '_yz_id': '1*nodes*default*{0}*{1}'.format(
                obj.key,
                random.randint(0, 100)
            ),
            'score': '1.0'
        }

        for subkey, type_subkey in obj.value:
            dockey = '{0}_{1}'.format(subkey, type_subkey)
            val = obj.value[(subkey, type_subkey)]

            if isinstance(val, frozenset):
                val = list(val)

            else:
                val = str(val)

            doc[dockey] = val

        docs.append(doc)

    return docs


mr = Middleware.get_middleware_by_uri(
    'mapreduce+multiprocessing:///r2?mapcb=map-forward&reducecb=reduce-forward'
)

inputs = c.fulltext_search('nodes', 'neighbors_counter:[2 TO *]')
result = mr(mr(inputs['docs']))

print(json.dumps(result, indent=4))
