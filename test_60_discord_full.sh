#!/bin/bash
echo "Start the bot in background..."
python main.py &
echo "Wait for bot to start and connect"
sleep 10
# TODO: launch distest bot
# TODO: kill all bots