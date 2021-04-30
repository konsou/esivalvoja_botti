# TODO: MORE OF THESE TESTS
from __future__ import annotations
import sys
import os
from typing import TYPE_CHECKING

from distest import TestCollector, TestInterface
from distest import run_dtest_bot
from distest.exceptions import ResponseDidNotMatchError
from discord import Message, User
from dotenv import load_dotenv

from app.response import load_responses

if TYPE_CHECKING:
    from app.response import ResponseList, AllResponses

load_dotenv()
test_collector = TestCollector()
ALL_RESPONSES: AllResponses = load_responses('app/json_data/responses.json')


@test_collector()
async def test_mention_dont_understand(interface):
    valid_responses: ResponseList = ALL_RESPONSES['dont_understand']

    def check_message_valid(message: Message) -> bool:
        result = any((valid_response in message.content for valid_response in valid_responses))
        if not result:
            print(f"invalid response: {message.content}. Should contain one of: {valid_responses}")
        return result

    await interface.send_message(f"Ymmärrätkös tätä <@{os.getenv('DISCORD_DEV_BOT_ID')}>")
    return await interface.wait_for_event("message",
                                          check=check_message_valid,
                                          timeout=5)


@test_collector()
async def test_mention_regret(interface):
    valid_responses: ResponseList = []
    valid_responses.extend(ALL_RESPONSES['positive'])
    valid_responses.extend(ALL_RESPONSES['negative'])

    tester_bot_id: int = int(os.getenv('DISCORD_TEST_BOT_ID'))
    tester_bot_user: User = interface.client.get_user(tester_bot_id)

    def check_message_valid(message: Message) -> bool:
        for valid_response in valid_responses:
            reponse_with_name = valid_response.replace('%name%', tester_bot_user.display_name)
            if reponse_with_name in message.content:
                return True

        # result = any((valid_response.replace('%name%', bot_user.display_name) in message.content for valid_response in valid_responses))
        
        print(f"invalid response: {message.content}. Should contain one of: {valid_responses}")
        return False

    await interface.send_message(f"Kadun kovasti! <@{os.getenv('DISCORD_DEV_BOT_ID')}>")
    return await interface.wait_for_event("message",
                                          check=check_message_valid,
                                          timeout=5)


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
async def test_dont_reply_to_everyone_or_here(interface):
    """
    Don't reply to @everyone and @here
    """
    await interface.send_message(f"@everyone")
    await interface.send_message(f"@here")
    await interface.ensure_silence()


if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)
