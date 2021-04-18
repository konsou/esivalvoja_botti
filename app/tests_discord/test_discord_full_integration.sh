#!/bin/bash
source .env
if [ ! -f "./main.py" ]; then
    echo "Run this script from the project root folder."
    exit 1
fi
echo "------------------------------------------"
echo "| RUNNING DISCORD FULL INTEGRATION TESTS |"
echo "------------------------------------------"
echo "Start the bot in background..."
python main.py &
BOT_PID=$!
echo "Bot PID is ${BOT_PID}"
echo "Wait for bot to start and connect..."
sleep 5
echo "Start the tester bot and run tests..."
PYTHONPATH=$(pwd)
export PYTHONPATH # set the currend working directory as PYTHONPATH. Needed for imports to work in the following script.
python app/tests_discord/tester_bot.py --channel "${DISCORD_TEST_CHANNEL_ID}" --run all "${DISCORD_DEV_BOT_ID}" "${DISCORD_TEST_CLIENT_TOKEN}"
TESTER_RESULT=$?

echo "Kill the bot..."
kill -9 $BOT_PID

if [ $TESTER_RESULT -eq 0 ]; then
    echo "TEST RESULT: OK"
else
    echo "TEST RESULT: FAIL"
fi

exit $TESTER_RESULT