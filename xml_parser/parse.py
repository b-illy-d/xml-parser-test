from __future__ import annotations

from contextlib import suppress
from typing import List

from lxml import etree

from .types import StreamLike


def parse_stream(
    source: StreamLike,
):
    parser = etree.iterparse(
        source,
        events=(
            "start",
            "end",
        ),
        recover=True,
        huge_tree=True,
    )

    epo_nums: List[str] = []
    patent_office_nums: List[str] = []
    try:
        in_application_reference = False
        for event, element in parser:
            if event == "end" and element.tag == "document-id":
                is_epo = element.attrib.get("format") == "epo"
                is_patent_office = element.attrib.get("load-source") == "patent-office"
                for child in element:
                    if child.tag == "doc-number":
                        if is_epo and child.text is not None:
                            epo_nums.append(child.text)
                        elif is_patent_office and child.text is not None:
                            patent_office_nums.append(child.text)
                element.clear(keep_tail=True)
            elif event == "start" and element.tag == "application-reference":
                in_application_reference = True
            elif event == "end" and element.tag == "application-reference":
                in_application_reference = False
            if event == "start" and not in_application_reference:
                element.clear(keep_tail=True)

    finally:
        with suppress(Exception):
            source.close()
    return epo_nums + patent_office_nums
