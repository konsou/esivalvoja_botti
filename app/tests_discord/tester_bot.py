# TODO: MORE OF THESE TESTS
import sys
import os

from distest import TestCollector, TestInterface
from distest import run_dtest_bot
from distest.exceptions import ResponseDidNotMatchError

from dotenv import load_dotenv

from app.response import load_responses

load_dotenv()

test_collector = TestCollector()
created_channel = None


@test_collector()
async def test_silence(interface):
    """
    Don't reply if not mentioned
    """
    await interface.send_message("Esivalvoja tai esivalvoja-testing: mitä kuuluu?")
    await interface.send_message("Testing for silence")
    await interface.send_message("Shhhhh...")
    await interface.ensure_silence()


@test_collector()
async def test_mention_dont_understand(interface):
    # TODO: Don't hardcode tester bot ID
    responses = load_responses('app/json_data/responses.json')
    await interface.send_message(f"<@{os.getenv('DISCORD_DEV_BOT_ID')}>")
    response = await interface.wait_for_message()
    if not any((valid_response in response.content for valid_response in responses['dont_understand'])):
        error_msg = f"invalid response: {response.content}. Should contain one of: {responses['dont_understand']}"
        # Raising ResponseDidNotMatchError doesn't print anything - need to print this manually
        print(error_msg)
        raise ResponseDidNotMatchError(error_msg)


@test_collector()
async def test_dont_reply_to_everyone_or_here(interface):
    """
    Don't reply to @everyone and @here
    """
    await interface.send_message(f"@everyone")
    await interface.send_message(f"@here")
    await interface.ensure_silence()


if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)
