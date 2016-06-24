#!/bin/bash

echo "-- Create bucket-type: nodes"
riak-admin bucket-type create nodes '{"props": {"datatype": "map"}}' 2>&1 >/dev/null || exit 1
echo "-- Create bucket-type: relationships"
riak-admin bucket-type create relationships '{"props": {"datatype": "map"}}' 2>&1 >/dev/null || exit 1
echo "-- Create bucket-type: graphs"
riak-admin bucket-type create graphs '{"props": {"datatype": "map"}}' 2>&1 >/dev/null || exit 1

echo "-- Activate bucket-type: nodes"
riak-admin bucket-type activate nodes 2>&1 >/dev/null || exit 1
echo "-- Activate bucket-type: relationships"
riak-admin bucket-type activate relationships 2>&1 >/dev/null || exit 1
echo "-- Activate bucket-type: graphs"
riak-admin bucket-type activate graphs 2>&1 >/dev/null || exit 1

python init.py || exit 1

echo "-- Set search index on bucket-type: nodes"
riak-admin bucket-type update nodes '{"props": {"search_index": "nodes"}}' 2>&1 >/dev/null || exit 1
echo "-- Set search index on bucket-type: relationships"
riak-admin bucket-type update relationships '{"props": {"search_index": "relationships"}}' 2>&1 >/dev/null || exit 1
echo "-- Set search index on bucket-type: graphs"
riak-admin bucket-type update graphs '{"props": {"search_index": "graphs"}}' 2>&1 >/dev/null || exit 1
