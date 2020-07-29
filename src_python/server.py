from flask import Flask, request, jsonify
import nerd
app = Flask(__name__)


@app.route('/api')
def api_home():
    return 42

@app.route('/api/v1', methods=['GET'])
def name_entity_disambiguate():
    # chunking
    entities = nerd.disambiguate(request.args.get('query'))
    if entities:
        return jsonify(entities)
    return jsonify({"error": "no entities"})
    return None
