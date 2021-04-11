#!/bin/bash
source .env
echo "Start the bot in background..."
python main.py &
BOT_PID=$!
echo "Bot PID is ${BOT_PID}"
echo "Wait for bot to start and connect"
sleep 10
# TODO: launch distest bot
# TODO: kill all bots
echo "Start the tester bot and run tests..."
python app/tests/example_tester.py --channel "${DISCORD_TEST_CHANNEL_ID}" --run all "${DISCORD_DEV_BOT_ID}" "${DISCORD_TEST_CLIENT_TOKEN}"
TESTER_RESULT=$?

echo "Killing the bot..."
kill -9 $BOT_PID

if [ $TESTER_RESULT -eq 0 ]; then
    echo "TEST RESULT: OK"
else
    echo "TEST RESULT: FAIL"
fi