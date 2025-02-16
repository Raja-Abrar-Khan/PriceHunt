from flask import Flask, request, jsonify
from googlesearch import search
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

@app.route("/searc", methods=["POST"])
def google_search():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    top_results = list(search(query, num_results=5))

    return jsonify({"results": top_results})

if __name__ == "__main__":
    app.run(debug=True)
