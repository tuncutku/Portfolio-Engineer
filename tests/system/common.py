"""Functions used in system tests"""

from datetime import datetime


def templete_used(expected_templates, captured_templates):
    """Check if a list of templates have been used during the system tests."""

    assert expected_templates == [
        template.name for template, context in captured_templates
    ]


def convert_date_to_string(
    data: dict, data_input: str, data_format: str = "%Y-%m-%d"
) -> dict:
    """Convert input to string."""

    if data.get(data_input):
        value: datetime = data[data_input]
        data[data_input] = value.strftime(data_format)
    return data
