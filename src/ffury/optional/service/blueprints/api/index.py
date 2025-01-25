from flask import (
    current_app,
    make_response
)

from . import api
from ...misc.status import get_flask_app_status


@api.route("/", methods=["GET"]) 
def index():
    """
    Validation connexion au service.
    ---
    responses:
      200:
        description: API is running
    """
    status = get_flask_app_status(current_app)
    return make_response(status)
