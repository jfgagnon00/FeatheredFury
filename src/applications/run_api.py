from waitress import serve
from api import create_api

api = create_api()

if __name__ == '__main__':
    #api.run(host='0.0.0.0', port=8000, debug=True)
    serve(api, host="0.0.0.0", port=8080)


# from api import create_api
# from flasgger import Swagger, swag_from

# api = create_api()

# api.config['SWAGGER']={'title':'Service de prediction de retard', 'version':'1.5.0'}

# if __name__ == '__main__':
#     swagger=Swagger(api)
#     api.run(host='0.0.0.0', port=8000, debug=True)