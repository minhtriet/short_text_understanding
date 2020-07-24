from flair.models import SequenceTagger
from flair.data import Sentence
from flask import Flask
import nerd
import wikidata_adapter

app = Flask(__name__)

tagger = SequenceTagger.load('chunk')
@app.route('/api')
def api_home():
    return 42;

@app.route('/api/v1', methods=['GET'])
def nerd():
    data = request.get_json(force=True)
    input_params = data['input']
    # chunking
    sentence = Sentence(input_params['sentence'])
    print(f'this tagger predicts the {tagger.tag_type} tag')
    tagger.predict(sentence)
    print(sentence)
    print('The following chunk tags are found:')
    for entity in sentence.get_spans('np'):
        print(entity)
        entity_dict = entity.to_dict()
        entity_dict['tag'] = entity.tag
        entity_dict['score'] = entity.score
    #{'text': 'buy', 'start_pos': 0, 'end_pos': 3, 'labels': [VP (0.9305)]}
    
    # nerd with wikidata
    wikidata = wikidata_adapter(data)
    entities = wikidata.to_entity_list()
