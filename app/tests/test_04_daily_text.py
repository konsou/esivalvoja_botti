import unittest
import asyncio
import platform
import datetime

from app.services.daily_text import daily_text, result_is_cached, _cached_result


# Prevent 'event loop is closed' error on Windows
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class TestDailyText(unittest.IsolatedAsyncioTestCase):
    async def test_has_contents(self):
        """
        Test that daily_text has contents
        """
        dtext = await daily_text()
        self.assertTrue(len(dtext), 'daily text has a length of more than 0')
        self.assertIsInstance(dtext, str, 'daily text is a string')

    async def test_cache(self):
        """
        Test daily_text cache
        """
        self.assertFalse(result_is_cached(), 'daily text should not be cached before first fetch')
        dtext = await daily_text()
        self.assertTrue(result_is_cached(), 'daily text should be cached after fetch')
        self.assertEqual(dtext, _cached_result.result, 'cached daily text matches actual')

    async def test_known_daily_text(self):
        """
        Test that a daily text for a given date matches actual text
        """
        expected_text = """**Minä näytän sinulle sen suuren prostituoidun tuomion. (Ilm. 17:1)**\n\nSuuri Babylon, väärän uskonnon maailmanmahti, on aiheuttanut paljon häpeää Jumalan nimelle. Se on opettanut valheita Jumalasta ja syyllistynyt hengelliseen prostituutioon liittoutumalla maan vallanpitäjien kanssa. Suuren vaikutusvaltansa avulla se on riistänyt jäseniään. Se on vuodattanut paljon verta, myös Jumalan palvelijoiden verta. (Ilm. 18:24; 19:2.) Jehova käyttää ”suuren prostituoidun” tuhoamiseen kirkkaanpunaisen pedon ”kymmentä sarvea”. Kuvaannollinen peto edustaa Yhdistyneitä kansakuntia, ja sen kymmenen sarvea edustavat nykyisiä poliittisia valtoja, jotka tukevat tätä järjestöä. Jumalan määräaikana poliittiset vallat kääntyvät Suurta Babylonia vastaan ja ”riisuvat hänet paljaaksi ja alastomaksi”. Ne ryöstävät hänen omaisuutensa ja paljastavat hänen pahuutensa. (Ilm. 17:3, 16.) Prostituoidun nopea tuho, joka tulee ikään kuin yhtenä päivänä, on järkytys hänen tukijoilleen, koska hän on pitkään kerskaillut: ”Minä – – en koskaan joudu kokemaan surua.” (Ilm. 18:7, 8.) w19.09 10 kpl:t 10–11"""
        date_for_text = datetime.datetime(year=2021, month=4, day=19)
        dtext = await daily_text(date=date_for_text)
        self.assertEqual(dtext, expected_text, f'daily_text for {date_for_text} matches expected_text')
