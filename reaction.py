from time import time
from random import choice, randint

LAST_REGRET_ALLOWED_INTERVAL = 60  # seconds

TOO_SOON_REACTIONS = [
    "Eiköhän tämä nyt tullut vähän liian nopeasti. Odottele jonkin aikaa niin katsotaan sitten.",
    "Kyllä katumukseen kuuluu se, että ei nyt ihan heti rupea samaa tekemään.",
]

NEGATIVE_REACTIONS = [
    "Et kyllä näytä *oikeasti* katuvan. On sellaista seurausten pahoittelua vain tuo.",
    "Kadut kyllä mutta tämä tapaus on nyt sen verran julkinen että sinusta pitää tehdä esimerkki.",
    "Syntisi oli teknisesti ottaen hyvin pieni mutta astuit Veli Vanhimman vaimon varpaille, joten erotus napsahtaa.",
    "Olisihan tässä näitä lieventäviä asianhaaroja mutta lätkäpeli alkaa kohta eikä kiinnosta.",
]

POSITIVE_REACTIONS = [
    "Totta kai saat anteeksi, rakas %name%! Katumuksesi on selvästi aitoa ja sinulla on aivan ilmeisesti Jehovan siunaus!",
    "Saat anteeksi tällä kertaa mutta rajoituksia kyllä tulee.",
    "Saat anteeksi mutta tästä kyllä ilmoitetaan lavalla että varmasti tunnet nahoissasi.",
    "KV on setäsi kummin kaima joten kaipa me jätetään tämä asia tähän.",
]


def get_reaction(user_name: str, last_regret_timestamp: float) -> str:
    print(f"In get_reaction - user_name: {user_name}, last_regret_timestamp: {last_regret_timestamp}")
    if (time() - last_regret_timestamp) < LAST_REGRET_ALLOWED_INTERVAL:
        reply_table = TOO_SOON_REACTIONS
    elif randint(0, 1) == 0:
        reply_table = NEGATIVE_REACTIONS
    else:
        reply_table = POSITIVE_REACTIONS

    reply = choice(reply_table)
    reply.replace('%name%', user_name)
    return f"{reply} @{user_name}"
