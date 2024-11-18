from flask import Blueprint, make_response, jsonify
#mettre dans requirement.txt flasgger
from flasgger import Swagger, swag_from
from .controller import ApiController


api_routes = Blueprint('api', __name__, url_prefix='/api')
api_controller = ApiController()
@api_routes.route('/', methods=['GET'])
def index():
    """ Example endpoint with simple greeting.
    ---
    tags:
      - Example API
    responses:
      200:
        description: A simple greeting
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                message:
                  type: string
                  example: "Hello World!"
    """
    result=api_controller.index()
    return make_response(jsonify(data=result))
      