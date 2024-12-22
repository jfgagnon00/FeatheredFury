from flask import make_response

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
    result = dict(status="API is running")
    return make_response(result)
