import os
import google.generativeai as genai
from flask import Blueprint , request , jsonify


genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  system_instruction="You are an experienced Software Engineer. Your name is AutoDev, who is expert in every aspect of software engineering"
)

chat = Blueprint('chat', __name__)


@chat.route("/", methods=['GET','POST'])
def get_response():
    if request.method == 'POST':
        prompt = request.json.get("prompt")
        # img = request.files
        res = model.generate_content(prompt)
        return jsonify({"message": res.text, "success": True})
    return "<h1>Chat Now</h1>"
        