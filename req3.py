# -*- coding: utf-8 -*-

from riak import RiakClient
import itertools
import random
import json


c = RiakClient(nodes=[{
    'host': '127.0.0.1',
    'pb_port': '8087'
}])


nodes = c.bucket_type('nodes').bucket('default')
relationships = c.bucket_type('relationships').bucket('default')
graphs = c.bucket_type('graphs').bucket('default')


def map_select(doc):
    targets = doc.get('targets_set', [])

    if not isinstance(targets, list):
        targets = [targets]

    rel_ids = []
    node_ids = []

    for target in targets:
        rel, node = target.split(':')
        rel_ids.append(rel)
        node_ids.append(node)

    return rel_ids, node_ids


def reduce_select(targets):
    rel_ids, node_ids = targets

    rel_objs = relationships.multiget(rel_ids)
    node_objs = nodes.multiget(node_ids)

    rel_docs = []
    node_docs = []

    for obj in rel_objs:
        doc = {
            '_yz_rt': 'relationships',
            '_yz_rb': 'default',
            '_yz_rk': obj.key,
            '_yz_id': '1*relationships*default*{0}*{1}'.format(
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

        rel_docs.append(doc)

    for obj in node_objs:
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

        node_docs.append(doc)

    return rel_docs, node_docs


n = c.fulltext_search('nodes', 'type_set:TB')

result = list(
    itertools.chain.from_iterable(
        map(
            reduce_select,
            map(
                map_select,
                n['docs']
            )
        )
    )
)

result_rels, result_nodes = result

print('Relations:')
print(json.dumps(result_rels, indent=4))

print('Nodes:')
print(json.dumps(result_nodes, indent=4))
