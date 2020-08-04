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

NOUN_TAG = 'NOUN'
PROPN_TAG = 'PROPN'
VERB_TAG = 'VERB'
ADJ_TAG = 'ADJ'

tagger = SequenceTagger.load('upos-fast')
flair_embedding_forward = FlairEmbeddings('news-forward')
flair_embedding_backward = FlairEmbeddings('news-backward')

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def sentence_similarity(sent_1, sent_2) -> float:
  if len(sent_1) == 0 or len(sent_2) == 0:
    return 0
  return max([np.dot(token_prime.embedding, token.embedding) 
              for token in sent_1 for token_prime in sent_2])


def disambiguate(query) -> List[Entity]:
    sentence = Sentence(query)
    tagger.predict(sentence)
    logging.log(logging.DEBUG, sentence)
    most_likely_entities = []
    trailing = 0
    token_index = 0
    total_prob, possible_entities = 0, None
    while token_index < len(sentence.tokens):
        token = sentence[token_index]
        if token.get_tag('pos').value in [NOUN_TAG, PROPN_TAG]:
            if token_index == len(sentence) - 1:
              longest_token_index = len(sentence)
            else:
              for longest_token_index in range(token_index + 1, len(sentence)):
                  if sentence[longest_token_index].get_tag('pos').value != NOUN_TAG:
                      break
            biggest_probs = float('-inf')
            best_config = (token_index, token_index)
            possible_entities = None
            # extract subtext with most claims in the database
            for start_index in range(token_index, longest_token_index):
                for end_index in range(start_index+1, longest_token_index + 1):
                    sub_text = ' '.join(list(map(lambda x: x.text, sentence[start_index:end_index])))
                    wikidata = wikidata_adapter.WikidataAdapter(sub_text)
                    total_prob, possible_entities = wikidata.to_entity_list()
                    if possible_entities[0].probability > biggest_probs:   # only consider most relevant entity
                        biggest_probs = total_prob
                        best_config = (start_index, end_index)
            # found an entity!!!
            # now what are the trailing tokens?
            # the var `trailing` is from previous entity!
            preceding_part = Sentence(' '.join(list(map(lambda x: x.text, sentence[trailing:best_config[0]]))))
            flair_embedding_forward.embed(preceding_part)
            # now updating `trailing`
            for trailing in range(best_config[1], len(sentence)):
                if sentence[trailing].get_tag('pos').value in [ADJ_TAG, VERB_TAG]:
                    break
            token_index = trailing + 1
            succeeding_part = Sentence(' '.join(list(map(lambda x: x.text, sentence[best_config[1]+1:trailing+1]))))
            flair_embedding_backward.embed(succeeding_part)
            # use words around that subtext to gain more data for likelihood
            if possible_entities:
                # get possible entities
                similarities = []
                if preceding_part or succeeding_part:
                    # reduce two arrays of embedding to a number of maximum similarity
                    for prob in possible_entities:
                        desc = Sentence(prob.description)
                        flair_embedding_forward.embed(desc)
                        best_sim = max(sentence_similarity(desc, preceding_part), sentence_similarity(desc, succeeding_part))
                        similarities.append(best_sim)
                    similarities = special.softmax(similarities)
                    # bayes rule
                    posteriors = similarities * [entity.probability for entity in possible_entities]
                    most_likely_index = np.argmax(posteriors)
                else:
                    most_likely_index = np.argmax([entity.probability for entity in possible_entities])
            possible_entities[most_likely_index].start_pos = best_config[0]
            possible_entities[most_likely_index].end_pos = best_config[1]
            most_likely_entities.append(possible_entities[most_likely_index])
        else:
            token_index += 1
    logging.log(logging.DEBUG, most_likely_entities)
    return most_likely_entities if most_likely_entities else None

