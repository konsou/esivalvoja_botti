#!/bin/bash
./test_printer.sh &
TEST_PID=$!
echo $TEST_PID
sleep 3
echo "Trying to kill"
kill -9 $TEST_PID