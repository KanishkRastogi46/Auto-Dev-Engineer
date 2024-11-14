import os
import google.generativeai as genai
from flask import Blueprint , request , jsonify , make_response
from flask_cors import cross_origin , CORS

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  system_instruction="You are an experienced Software Engineer. Your name is AutoDev, who is expert in every aspect of software engineering"
)

chat = Blueprint('chat', __name__)

CORS(chat , origins=["http://localhost:3000"])


@chat.route("/", methods=['GET','POST'])
@cross_origin()
def get_response():
    if request.method == 'POST':
        prompt = request.json.get("prompt")
        # img = request.files
        try:            
            result = model.generate_content(prompt)
            response = make_response(jsonify({"message": result.text, "success": True})) 
            return response
        except Exception as e:
            return jsonify({"message": str(e), "success": True})
    return "<h1>Chat Now</h1>"


@chat.route("/u")
def u():
    return jsonify({"message" : "hello"})
        