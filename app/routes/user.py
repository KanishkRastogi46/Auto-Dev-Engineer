from flask import Blueprint , jsonify , request , render_template
from app.models.user import User
from app import db
import uuid
from bcrypt import hashpw , gensalt , checkpw


user = Blueprint('user', __name__)

@user.route("/")
def root():
    return jsonify({'message': 'Users route'})


@user.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        fullname = request.json.get("fullname")
        email = request.json.get("email")
        password = request.json.get("password").encode('utf-8')
        hashed_password = hashpw(password , gensalt(rounds=10))
        
        user = User(id = str(uuid.uuid4()), fullname = fullname, email = email, password = hashed_password.decode('utf-8'))
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'User created', 'success':True})
        except Exception as e:
            return jsonify({'message': str(e), 'success': False})
    
    return render_template('register.html')
