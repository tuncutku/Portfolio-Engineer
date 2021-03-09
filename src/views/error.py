from flask import Blueprint, request, session, url_for, render_template, redirect
from flask_login import login_required, current_user
from werkzeug.exceptions import HTTPException


error_handler_blueprint = Blueprint(
    "error_handler", __name__, url_prefix="/error_handler"
)


@error_handler_blueprint.errorhandler(HTTPException)
def handle_exception(e):
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