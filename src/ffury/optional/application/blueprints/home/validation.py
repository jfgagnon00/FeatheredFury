from flask import (
    current_app,
    request,
    redirect,
)
from ffury.optional.application.misc.errors import log_error
from requests import post

from . import home


@home.route("/validation", methods=["GET", "POST"]) 
def validation():
    try:
        response = post(current_app.config["SERVICE_CONFIG"].validation_url,
                        json=request.get_json())

        if response.status_code != 200:
            return log_error(response.text), 400
        
        return redirect("/")
    except Exception as e:
        return log_error(repr(e)), 400
