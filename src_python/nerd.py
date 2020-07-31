"""
I implement this as a module instead of a class as it is intended to be a singleton
https://stackoverflow.com/a/6760726
"""

import wikidata_adapter
from base_adapter import Entity
from flair.models import SequenceTagger
from flair.data import Sentence
from typing import List
from flair.embeddings import WordEmbeddings, FlairEmbeddings
from scipy import special
import numpy as np

import sys
import logging

tagger = SequenceTagger.load('chunk')
NOUN_PHRASE_TAG = 'NP'
VERB_PHRASE_TAG = 'VP'
tagger = SequenceTagger.load('pos')


flair_embedding_forward = FlairEmbeddings('news-forward')
flair_embedding_backward = FlairEmbeddings('news-backward')

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def disambiguate(query) -> List[Entity]:
    sentence = Sentence(query)
    tagger.predict(sentence)
    logging.log(logging.DEBUG, sentence)
    print('The following chunk tags are found:')
    most_likely_entities = []
    effective_verb_embedding = ''
    for entity in sentence.get_spans('np'):
        if entity.tag == NOUN_PHRASE_TAG:
            print(entity)
            biggest_probs = 0
            best_config = (0, len(entity))
            best_entities = None
            # extract subtext with most claims
            for start_index in range(1, len(entity) - 1):
                for end_index in range(start_index+1, len(entity)):
                    sub_text = ' '.join(list(map(lambda x: x.text, entity.tokens[start_index:end_index+1])))
                    wikidata = wikidata_adapter.WikidataAdapter(sub_text)
                    total_prob, possible_entities = wikidata.to_entity_list()
                    if total_prob > biggest_probs:
                        biggest_probs = total_prob
                        best_entities = possible_entities
                        best_config = (start_index, end_index)
            # use words around that subtext to gain more data for likelihood
            if best_entities:
                similarities = []
                if effective_verb_embedding:
                    # reduce two arrays of embedding to a number of maximum similarity
                    for prob in possible_entities:
                        desc = Sentence(prob.description)
                        flair_embedding_forward.embed(desc)
                        similarities.append(max([np.dot(token_prime.embedding, token.embedding) for token in desc for token_prime in effective_verb_embedding]))
                    similarities = special.softmax(similarities)
                    # bayes rule
                    posteriors = similarities * [entity.probability for entity in possible_entities]
                    most_likely_index = np.argmax(posteriors)
                else:
                    most_likely_index = np.argmax([entity.probability for entity in possible_entities])
            possible_entities[most_likely_index].start_pos = entity.start_pos
            possible_entities[most_likely_index].end_pos = entity.end_pos
            most_likely_entities.append(possible_entities[most_likely_index])
            if entity.tag == VERB_PHRASE_TAG:
                effective_verb_embedding = Sentence(entity.text)
                flair_embedding_forward.embed(effective_verb_embedding)
    logging.log(logging.DEBUG, most_likely_entities)
    return most_likely_entities if most_likely_entities else None

