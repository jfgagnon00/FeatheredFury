from flask import Flask


def get_flask_app_status(app: Flask) -> dict:
    return dict(
        controller=app.config["CONTROLLER"].status,
    )
