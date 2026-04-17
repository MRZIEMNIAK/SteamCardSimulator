# game state management


def _cards(*entries):
    """Build card dicts from tuples: (name, drop_rate)."""
    return [
        {"id": idx + 1, "name": name, "drop_rate": drop_rate}
        for idx, (name, drop_rate) in enumerate(entries)
    ]


#list of games and their respective card drops and drop rates
games = [
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
        "total_cards": 0,
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
        "total_cards": 0,
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
        "total_cards": 0,
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
        "total_cards": 0,
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
        "total_cards": 0,
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
        "total_cards": 0,
    },
]





