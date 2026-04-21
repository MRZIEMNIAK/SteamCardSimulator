"""
Card and game catalog for the Steam Card Drop Simulator.

Veikka
"""

import copy

# cards id, name, drop_rate, rarity, value
def _cards(*entries, rarity="common", value=None):
    """Build card dicts from tuples: (name, drop_rate)."""
    card_value = value if value is not None else (10 if rarity == "rare" else 5)
    return [
        {"id": idx + 1, "name": name, "drop_rate": drop_rate, "rarity": rarity, "value": card_value}
        for idx, (name, drop_rate) in enumerate(entries)
    ]


# list of default games and their respective card drops, drop rates
DEFAULT_GAMES = [
    {
        "id": 1,
        "name": "DOTA 2",
        "cards": _cards(
            ("Axe", 0.20),
            ("Invoker", 0.12),
            ("Crystal Maiden", 0.22),
            ("Pudge", 0.15),
            ("Juggernaut", 0.18),
        ),
        "rare_cards": _cards(
            ("Arcana Axe", 0.04),
            ("Immortal Invoker", 0.03),
            rarity="rare",
        ),
        "total_cards": 7,
    },
    {
        "id": 2,
        "name": "Team Fortress 2",
        "cards": _cards(
            ("Scout", 0.24),
            ("Heavy", 0.17),
            ("Spy", 0.14),
            ("Engineer", 0.19),
            ("Medic", 0.21),
        ),
        "rare_cards": _cards(
            ("Golden Scout", 0.04),
            ("Strange Spy", 0.03),
            rarity="rare",
        ),
        "total_cards": 7,
    },
    {
        "id": 3,
        "name": "Counter-Strike: Global Offensive",
        "cards": _cards(
            ("Dust II", 0.20),
            ("Mirage", 0.19),
            ("Inferno", 0.17),
            ("AWP", 0.13),
            ("Defuse Kit", 0.22),
        ),
        "rare_cards": _cards(
            ("StatTrak AWP", 0.03),
            ("Ancient Mirage", 0.04),
            rarity="rare",
        ),
        "total_cards": 7,
    },
    {
        "id": 4,
        "name": "PAYDAY 2",
        "cards": _cards(
            ("Dallas", 0.21),
            ("Chains", 0.20),
            ("Hoxton", 0.17),
            ("Clover", 0.16),
            ("The Heist", 0.19),
        ),
        "rare_cards": _cards(
            ("Diamond Dallas", 0.04),
            ("Overkill Heist", 0.03),
            rarity="rare",
        ),
        "total_cards": 7,
    },
    {
        "id": 5,
        "name": "Portal 2",
        "cards": _cards(
            ("Chell", 0.18),
            ("GLaDOS", 0.12),
            ("Wheatley", 0.20),
            ("Atlas", 0.22),
            ("P-Body", 0.22),
        ),
        "rare_cards": _cards(
            ("Blue Portal", 0.04),
            ("Aperture Prototype", 0.03),
            rarity="rare",
        ),
        "total_cards": 7,
    },
    {
        "id": 6,
        "name": "Left 4 Dead 2",
        "cards": _cards(
            ("Coach", 0.20),
            ("Ellis", 0.19),
            ("Nick", 0.18),
            ("Rochelle", 0.21),
            ("Tank", 0.10),
        ),
        "rare_cards": _cards(
            ("Infected Tank", 0.03),
            ("Last Stand Rochelle", 0.04),
            rarity="rare",
        ),
        "total_cards": 7,
    },
]

games = copy.deepcopy(DEFAULT_GAMES)





