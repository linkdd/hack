# -*- coding: utf-8 -*-

from riak import RiakClient


c = RiakClient(nodes=[{
    'host': '127.0.0.1',
    'pb_port': '8087'
}])


nodes = c.bucket_type('nodes').bucket('default')
relationships = c.bucket_type('relationships').bucket('default')
graphs = c.bucket_type('graphs').bucket('default')


ta = nodes.new('ta')
ta.sets['type'].add('TA')
ta.sets['targets'].add('r1:tb')
ta.sets['targets'].add('r3:tc')
ta.sets['targets'].add('r4:tc')
ta.counters['neighbors'].increment(2)
ta.counters['n_targets'].increment(3)
ta.counters['n_rels'].increment(3)
ta.store()

tb = nodes.new('tb')
tb.sets['type'].add('TB')
tb.sets['targets'].add('r2:tc')
tb.counters['neighbors'].increment(2)
tb.counters['n_targets'].increment(1)
tb.counters['n_rels'].increment(2)
tb.store()

tc = nodes.new('tc')
tc.sets['type'].add('TC')
tc.counters['neighbors'].increment(3)
tc.counters['n_rels'].increment(4)
tc.store()

td = nodes.new('td')
td.sets['type'].add('TD')
td.sets['targets'].add('r5:tc')
td.counters['neighbors'].increment(1)
td.counters['n_targets'].increment(1)
td.counters['n_rels'].increment(1)
td.store()

r1 = relationships.new('r1')
r1.sets['type'].add('X')
r1.flags['directed'].enable()
r1.registers['weight'].assign('1')
r1.store()

r2 = relationships.new('r2')
r2.sets['type'].add('X')
r2.flags['directed'].enable()
r2.registers['weight'].assign('1')
r2.store()

r3 = relationships.new('r3')
r3.sets['type'].add('Y')
r3.flags['directed'].enable()
r3.registers['weight'].assign('1')
r3.store()

r4 = relationships.new('r4')
r4.sets['type'].add('X')
r4.flags['directed'].enable()
r4.registers['weight'].assign('1')
r4.store()

r5 = relationships.new('r5')
r5.sets['type'].add('Y')
r5.flags['directed'].enable()
r5.registers['weight'].assign('1')
r5.store()

g1 = graphs.new('g1')
g1.sets['type'].add('G')

for n in ['ta', 'tb', 'tc', 'td']:
    g1.sets['nodes'].add(n)

for r in ['r1', 'r2', 'r3', 'r4', 'r5']:
    g1.sets['rels'].add(r)

g1.store()
