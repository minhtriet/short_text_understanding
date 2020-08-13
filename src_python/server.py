from flask import Flask, request, jsonify
import nerd
app = Flask(__name__)


@app.route('/')
def api_home():
    return "42"

@app.route('/api/v1', methods=['GET'])
def name_entity_disambiguate():
    entities = nerd.disambiguate(request.args.get('query'))
    if entities:
        return jsonify(entities)
    return jsonify({"error": "no entities"})


@app.route('/api/v2', methods=['GET'])
def name_entity_disambiguate_v2():
    entities = nerd.disambiguate_v2(request.args.get('query'))
    if entities:
        return jsonify(entities)
    return jsonify({"error": "no entities"})
