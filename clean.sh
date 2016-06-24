#!/bin/bash

echo "-- Stopping Riak"
service riak stop 2>&1 >/dev/null || exit 1
echo "-- Cleaning Riak"
rm -rf /var/lib/riak/* 2>&1 >/dev/null || exit 1
echo "-- Starting Riak"
service riak start 2>&1 >/dev/null || exit 1
