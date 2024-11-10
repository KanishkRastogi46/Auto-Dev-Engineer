from app import create_app
from flask_cors import CORS

app = create_app()

if __name__=="__main__":
    CORS(app=app, supports_credentials=True)
    app.run(debug=True)