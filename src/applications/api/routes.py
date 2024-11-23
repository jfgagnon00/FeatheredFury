import json
import logging
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
      

@api_routes.route('/waveform', methods=['POST']) 
def waveform(): 
    result=api_controller.waveform()
    #logging.info(f"****************************: {result.get_json() if result.is_json else result.data.decode('utf-8')}")
    return make_response(result)