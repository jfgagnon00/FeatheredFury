from flask import (
    current_app,
    make_response,
    request
)

from . import api


@api.route("/validation", methods=["GET", "POST"]) 
def validation():
    """
    Validation connexion au service.
    ---
    responses:
      200:
        description: TODO
    """
    print("AstieQ@#$!@#$!@#$")
    current_app.config["LOGGER"].info(request.get_json())
    return make_response( dict(status="OK") )
