#!/bin/bash
# wait-for-it.sh

host=$1
shift
port=$1
shift
cmd="$@"

until nc -z $host $port; do
  echo "Waiting for $host:$port to be ready..."
  sleep 2
done

echo "$host:$port is up - executing command"
exec $cmd
