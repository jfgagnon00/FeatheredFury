from flask import (
    current_app,
    render_template
)


def log_error(message: str):
    current_app.config["LOGGER"].error(message)
    return render_template("errors/oups.html",
                           error_message=message)
