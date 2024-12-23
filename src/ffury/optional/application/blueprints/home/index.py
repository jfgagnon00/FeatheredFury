from flask import (
    current_app,
    render_template
)

from . import home

@home.route("/", methods=["GET"])
def index(): 
    return render_template("home/index.html",
                           allowed_extensions=", ".join(current_app.config["ALLOWED_EXTENSIONS"]),
                           max_centent_length=current_app.config["MAX_CONTENT_LENGTH"] // 1024 // 1024 )
