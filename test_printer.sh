#!/bin/bash
counter=0
while true; do
    echo "test_printer: ${counter}"
    counter=$((counter+1))
    sleep 1
done
