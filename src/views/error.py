"""Error endpoints"""

# pylint: disable=invalid-name


import json
from flask import Blueprint
from werkzeug.exceptions import HTTPException


error_handler_blueprint = Blueprint(
    "error_handler", __name__, url_prefix="/error_handler"
)


@error_handler_blueprint.errorhandler(HTTPException)
def handle_exception(e):
    """Exception handling."""

    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response
