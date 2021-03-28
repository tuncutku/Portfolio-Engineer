def templete_used(expected_templates, captured_templates):
    assert expected_templates == [
        template.name for template, context in captured_templates
    ]
