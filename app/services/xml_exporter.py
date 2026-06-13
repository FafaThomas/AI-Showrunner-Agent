import xml.etree.ElementTree as ET

from app.models.schedule import DailySchedule


def schedule_to_xml(
    schedule: DailySchedule,
    target_date: str,
) -> str:
    """
    Convert a validated DailySchedule
    into XML.
    """

    root = ET.Element(
        "schedule",
        attrib={
            "date": target_date
        }
    )

    # ==========================
    # Theme
    # ==========================

    theme = ET.SubElement(
        root,
        "theme"
    )

    theme.text = schedule.theme

    # ==========================
    # Slots
    # ==========================

    for item in schedule.slots:

        slot = ET.SubElement(
            root,
            "slot"
        )

        ET.SubElement(
            slot,
            "slot_key"
        ).text = str(item.slot_key)

        ET.SubElement(
            slot,
            "time"
        ).text = item.time

        ET.SubElement(
            slot,
            "program_key"
        ).text = str(item.program_key)

        ET.SubElement(
            slot,
            "reason"
        ).text = item.reason

    # ==========================
    # Pretty Print
    # ==========================

    ET.indent(
        root,
        space="    ",
    )

    return ET.tostring(
        root,
        encoding="unicode",
    )

def save_xml(
    xml_content: str,
    filename: str,
):
    """
    Save XML to disk.
    """

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as f:
        f.write(xml_content)
