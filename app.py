import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.model import get_response

#Load environment variables
load_dotenv()

os.system("python backend/ingest_data.py")

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("query", "")
    
    if not user_query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        response = get_response(user_query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
    