from flask import Blueprint , jsonify , request , render_template , make_response
from app.models.user import User
from app import db
import uuid
from bcrypt import hashpw , gensalt , checkpw
import jwt
from flask_cors import cross_origin , CORS
import google.generativeai as genai
import os
import json


genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  system_instruction='''
  You are an experienced Software Engineer. Your name is AutoDev, who is expert in every aspect of Computer Science your task is to provide solution and response to only those questions or prompt which is related to software projects or programming  but if any question is asked outside the field of Computer Science simply respond with - "I'm sorry, but I can't respond to these queries".
  If any coding related question is asked then the response must be a JSON object which should have a following schema:
    1. Programming language: The name of language
    2. Code: The code along with proper indentation
    3. Explanation: The step-by-step guide for the code
    4. Note: Some points to remember, edge cases or scenarios
  If any theoretical question is asked just provide an explanation for the question asked.
  '''
)

user = Blueprint('user', __name__)

CORS(user , supports_credentials=True, origins=["http://localhost:3000"])


@user.route("/")
@cross_origin()
def root():
    users = User.query.all()
    data = []
    for user in users:
        data.append(user.to_dict())
    data.append({"access_token": request.cookies.get("access_token")})
    response = make_response(jsonify(data))
    return response


@user.route("/chat", methods=['GET','POST'])
@cross_origin()
def get_response():
    if request.method == 'POST':
        prompt = request.json.get("prompt")
        # img = request.files
        try:            
            result = model.generate_content(prompt)
            arr = result.text.split("```json\n")[1].split("\n```\n")[0]
            res = json.loads(arr)
            print(result.text)
            response = make_response(jsonify({"message": res, "success": True})) 
            return response
        except Exception as e:
            return jsonify({"message": str(e), "success": False})
    return "<h1>Chat Now</h1>"


# register route
@user.route("/register", methods=['GET','POST'])
@cross_origin()
def register():
    if request.method == 'POST':
        fullname = request.json.get("fullname")
        email = request.json.get("email")
        password = request.json.get("password")
        confirm_password = request.json.get("confirmPassword")
        
        try:
            if password != confirm_password:
                message = "Passwords doesn't match"
                print(message)
                return jsonify({"message": message, "success": False})
            
            else:
                find_user = User.query.filter_by(email=email).first()
                if find_user:
                    message = f"User with the same {find_user.email} already exists"
                    print(message)
                    return jsonify({"message": message, "success": False})
                
                hashed_password = hashpw(password.encode("utf-8") , gensalt())
                new_user = User(id = str(uuid.uuid4()), fullname = fullname, email = email, password = hashed_password.decode('utf-8'))
                db.session.add(new_user)
                db.session.commit()
                return jsonify({'message': 'User created', 'success':True})
        except Exception as e:
            return jsonify({'message': str(e), 'success': False})    
    return render_template('register.html')


# login route
@user.route("/login", methods=["GET", "POST"])
@cross_origin()
def login():
    if request.method == "POST":
        print(request.json)
        email = request.json.get("email")
        password = request.json.get("password").encode("utf-8")

        find_user = User.query.filter_by(email=email).first()
        if find_user:
            check_password = checkpw(password, find_user.password.encode('utf-8'))
            if not check_password:
                return jsonify({"message": "Incorrect password", "success": False})
            else:
                encoded = jwt.encode(payload={"id": find_user.id, "email": find_user.email}, key="bsdkmadarchod")
                res = make_response(jsonify({"message": "Login successfull", "success": True, "access_token": encoded}))
                # res.headers['Access-Control-Allow-Credentials'] = True
                res.set_cookie("access_token", value=encoded, httponly=True)
                return res
        else:
            return jsonify({"message": "User doesn't exists", "success": False})        
    return render_template("login.html")


# verify email
@user.route('/verify-email/<verify_token>', methods=['GET','POST'])
def verify_mail(verify_token):
    if request.method == "POST":
        user = User.query.filter_by(email = request.json.get("email")).first()
        if not user:
            return jsonify({"message": "Incorrect email", "success": False})
        else:
            return jsonify({"message": "Verification successfull", "success": True})
    return render_template("verify_email.html")


# change password
@user.route('/change-password/<email>', methods=['GET','POST'])
def change_password(email):
    if request.method == "POST":
        old_password = request.json.get("oldPassword").encode("utf-8")
        user = User.query.filter_by(email = email).first()
        if not checkpw(old_password, user.password.encode("utf-8")):
            return jsonify({"message": "Incorrect password", "success": False})
        else:
            new_password = request.json.get("newPassword").encode("utf-8")
            hashed_password = hashpw(new_password, gensalt())
            user.password = hashed_password.decode("utf-8")
            try:
                db.session.commit()
                return jsonify({"message": "Password changes successfully", "success": True})
            except Exception as e:
                return jsonify({"message": str(e), "success": False})
    return render_template("change_password.html")


# reset password
@user.route("/reset-password/<email>", methods=['GET', 'POST'])
def reset_password(email):
    return render_template("reset_password.html")


# logout route
@user.route("/logout")
def logout():
    res = make_response(jsonify({"message": "Logout successfull", "success": True}))
    res.delete_cookie("access_token")
    return res    