from app.models.schedule import DailySchedule


def validate_schedule(
    schedule: DailySchedule,
    slots: list,
    programs: list,
):
    """
    Validate that the generated schedule
    conforms to business rules.
    """

    expected_slot_count = len(slots)

    valid_slot_keys = {
        slot["slot_key"]
        for slot in slots
    }

    valid_program_keys = {
        program["program_key"]
        for program in programs
    }

    # ===================================
    # Check slot count
    # ===================================

    if schedule.slot_count != expected_slot_count:

        return False, (
            f"Expected {expected_slot_count} slots "
            f"but received {schedule.slot_count}."
        )

    # ===================================
    # Validate slot assignments
    # ===================================

    used_slot_keys = set()

    for slot in schedule.slots:

        # -------------------------------
        # Valid slot?
        # -------------------------------

        if slot.slot_key not in valid_slot_keys:

            return False, (
                f"Invalid slot_key: "
                f"{slot.slot_key}"
            )

        # -------------------------------
        # Valid program?
        # -------------------------------

        if slot.program_key not in valid_program_keys:

            return False, (
                f"Invalid program_key: {slot.program_key}"
            )

        # -------------------------------
        # Duplicate slot?
        # -------------------------------

        if slot.slot_key in used_slot_keys:

            return False, (
                f"Duplicate slot assignment: "
                f"{slot.slot_key}"
            )

        used_slot_keys.add(slot.slot_key)

    return True, None