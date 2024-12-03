from waitress import serve
from app import create_app

# Créer l'application Flask
app = create_app()


if __name__ == "__main__":
    # Lancer le serveur
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=5000)
    
# if __name__ == '__main__':
#     HOST = environ.get('SERVER_HOST', 'localhost')
#     try:
#         PORT = int(environ.get('SERVER_PORT', '5555'))
#     except ValueError:
#         PORT = 5555
#     app.run(HOST, PORT, debug=True)
 
