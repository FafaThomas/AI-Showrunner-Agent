# app/services/editorial_review.py

def review_schedule(
    schedule,
    programs,
    theme,
):
    """
    Editorial review of a generated schedule.

    Returns:
        (True, None)
        or
        (False, [feedback...])
    """

    feedback = []

    program_lookup = {
        p["program_key"]: p
        for p in programs
    }

    # -----------------------------------
    # Weekend Adventure checks
    # -----------------------------------

    if theme == "Weekend Adventure":

        prime_time = schedule.slots[18:23]

        prime_genres = [
            program_lookup[slot.program_key]["genre"]
            for slot in prime_time
        ]

        sitcom_count = prime_genres.count("Sitcom")

        if sitcom_count >= 3:
            feedback.append(
                "Prime Time contains too many sitcoms "
                "for a Weekend Adventure theme."
            )

        adventure_genres = {
            "Fantasy",
            "Action",
            "Sci-Fi",
            "Crime",
        }

        if not any(
            genre in adventure_genres
            for genre in prime_genres
        ):
            feedback.append(
                "Prime Time lacks adventurous flagship content."
            )

    # -----------------------------------
    # Morning checks
    # -----------------------------------

    morning = schedule.slots[6:12]

    morning_genres = [
        program_lookup[slot.program_key]["genre"]
        for slot in morning
    ]

    sci_fi_count = morning_genres.count("Sci-Fi")

    if sci_fi_count >= 4:
        feedback.append(
            "Morning programming feels too niche and Sci-Fi heavy."
        )

    crime_count = morning_genres.count("Crime")

    if crime_count >= 3:
        feedback.append(
            "Morning programming feels too dark."
        )

    # -----------------------------------
    # Final verdict
    # -----------------------------------

    if feedback:
        return False, feedback

    return True, None