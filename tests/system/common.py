"""Functions used in system tests."""


def templete_used(expected_templates, captured_templates):
    """Check if a list of templates have been used during the system tests."""

    assert expected_templates == [
        template.name for template, context in captured_templates
    ]
