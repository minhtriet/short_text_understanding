from flair.models import SequenceTagger
from flair.data import Sentence
from flask import Flask, request, jsonify
import sys
import logging

# import nerd
import wikidata_adapter

app = Flask(__name__)

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

tagger = SequenceTagger.load('chunk')

@app.route('/api')
def api_home():
    return 42;

@app.route('/api/v1', methods=['GET'])
def nerd():
    # chunking
    sentence = Sentence(request.args.get('query'))
    tagger.predict(sentence)
    print(sentence)
    print('The following chunk tags are found:')
    entities = []
    for entity in sentence.get_spans('np'):
        print(entity)
        entity_dict = entity.to_dict()
        entity_dict['tag'] = entity.tag
        entity_dict['score'] = entity.score
        # {'text': 'buy', 'start_pos': 0, 'end_pos': 3, 'labels': [VP (0.9305)]}
        # nerd with wikidata
        wikidata = wikidata_adapter.WikidataAdapter(entity_dict['text'])
        entities.append(wikidata.to_entity_list())
    logging.log(entities)
    return jsonify(entities)
