from flask import Flask, request, jsonify
from flask_cors import CORS

import nerd
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://minhtriet.github.io/short_text_understanding/"}})


@app.route('/')
def api_home():
    return "42"

@app.route('/api/v1', methods=['GET'])
def name_entity_disambiguate():
    # chunking
    entities = nerd.disambiguate(request.args.get('query'))
    if entities:
        return jsonify(entities)
    return jsonify({"error": "no entities"})
    return None
