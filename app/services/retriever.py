def retrieve_programs(
    programs,
    theme,
    slot,
):
    """
    Return programs relevant to the
    current theme and slot.
    """

    daypart = slot["daypart"]

    genre_map = {
        "Overnight": {
            "Sci-Fi",
            "Drama",
            "Reality",
            "Fantasy",
        },

        "Morning": {
            "Sitcom",
            "Reality",
            "Romance",
            "Special",
        },

        "Afternoon": {
            "Sitcom",
            "Romance",
            "Reality",
            "Fantasy",
        },

        "Prime Time": {
            "Fantasy",
            "Action",
            "Crime",
            "Sci-Fi",
        },

        "Late Night": {
            "Crime",
            "Drama",
            "Sci-Fi",
        },
    }

    allowed = genre_map.get(
        daypart,
        set(),
    )

    candidates = [
        p
        for p in programs
        if p["genre"] in allowed
    ]

    return candidates