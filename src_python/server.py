from flair.data import Sentence
from flair.models import SequenceTagger
from flair.data import Sentence
from flask import Flask
app = Flask(__name__)

tagger = SequenceTagger.load('chunk')
@app.route('/api')
def api_home():
    return 42;

@app.route('/nerd_api/v1', method='POST')
def nerd(query):
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
    # nerd with wikidata
    # class entity maybe
