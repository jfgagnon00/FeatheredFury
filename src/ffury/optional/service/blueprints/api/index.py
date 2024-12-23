from flask import (
    current_app,
    make_response
)

from . import api


@api.route("/", methods=["GET"]) 
def index():
    """
    Validation connexion au service.
    ---
    responses:
      200:
        description: API is running
    """
    return make_response( current_app.config["CONTROLLER"].status )
