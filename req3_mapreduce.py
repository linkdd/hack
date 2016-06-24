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


@register('map-select')
def map_select(mapper, node):
    targets = node.get('targets_set', [])

    if not isinstance(targets, list):
        targets = [targets]

    for target in targets:
        rel_id, node_id = target.split(':')

        mapper.emit('select-rel', rel_id)
        mapper.emit('select-node', node_id)


@register('reduce-select')
def reduce_select(reducer, key, ids):
    if key == 'select-rel':
        bucket_type = 'relationships'
        store = relationships

    elif key == 'select-node':
        bucket_type = 'nodes'
        store = nodes

    else:
        return []

    objs = store.multiget(ids)
    docs = []

    for obj in objs:
        doc = {
            '_yz_rt': bucket_type,
            '_yz_rb': 'default',
            '_yz_rk': obj.key,
            '_yz_id': '1*{0}*default*{1}*{2}'.format(
                bucket_type,
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
    'mapreduce+ipython:///req3?mapcb=map-select&reducecb=reduce-select'
)

inputs = c.fulltext_search('nodes', 'type_set:TB')
result = mr(inputs['docs'])

result_rels, result_nodes = result

print('Relations:')
print(json.dumps(result_rels, indent=4))

print('Nodes:')
print(json.dumps(result_nodes, indent=4))
