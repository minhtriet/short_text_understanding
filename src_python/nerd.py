"""
I implement this as a module instead of a class as it is intended to be a singleton
https://stackoverflow.com/a/6760726
"""

import wikidata_adapter
import wikidata_adapter_v2

from base_adapter import Entity
from flair.models import SequenceTagger
from flair.data import Sentence, Token
from typing import List
from flair.embeddings import FlairEmbeddings, PooledFlairEmbeddings, StackedEmbeddings
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

embedding_types = [
    PooledFlairEmbeddings('news-forward', pooling='min'),
    PooledFlairEmbeddings('news-backward', pooling='min'),
]
embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)


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
        # todo: change this to binary search, maybe to v2
        token = sentence[token_index]
        if token.get_tag('pos').value in [NOUN_TAG, PROPN_TAG]:
            if token_index == len(sentence) - 1:
              longest_token_index = len(sentence)
            else:
              for longest_token_index in range(token_index + 1, len(sentence)):
                  if sentence[longest_token_index].get_tag('pos').value in [NOUN_TAG, PROPN_TAG]:
                      break
            biggest_probs = float('-inf')
            best_config = (token_index, token_index)
            possible_entities = None
            # extract subtext with most claims in the database
            for start_index in range(token_index, longest_token_index):
                for end_index in range(start_index, longest_token_index + 1):
                    sub_text = ' '.join(list(map(lambda x: x.text, sentence[start_index:end_index+1])))  # end_index included
                    wikidata = wikidata_adapter.WikidataAdapter(sub_text)
                    total_prob, temp_possible_entities = wikidata.to_entity_list()
                    if temp_possible_entities and temp_possible_entities[0].probability > biggest_probs:   # only consider most relevant entity
                        biggest_probs = temp_possible_entities[0].probability
                        best_config = (start_index, end_index)
                        possible_entities = temp_possible_entities
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
                    for entity in possible_entities:
                        desc = Sentence(entity.description)
                        flair_embedding_forward.embed(desc)
                        best_sim = max(sentence_similarity(desc, preceding_part), sentence_similarity(desc, succeeding_part))
                        similarities.append(best_sim)
                    similarities = special.softmax(similarities)
                    # bayes rule
                    # posteriors = similarities * [entity.probability for entity in possible_entities]
                    # most_likely_index = np.argmax(posteriors)
                    most_likely_index = np.argmax(similarities)   # bayes rule seems does not work
                else:
                    most_likely_index = np.argmax([entity.probability for entity in possible_entities])
            possible_entities[most_likely_index].start_pos = sentence[best_config[0]].start_pos
            possible_entities[most_likely_index].end_pos = sentence[best_config[1]].end_pos
            most_likely_entities.append(possible_entities[most_likely_index])
        else:
            token_index += 1
    logging.log(logging.DEBUG, most_likely_entities)
    return most_likely_entities if most_likely_entities else None


def _join_text_flair(l: List[Token]) -> str:
    return ' '.join(list(map(lambda x: x.text, l)))

def _longest_entity(sentence, begin) -> int:
    """
    What is the longest consecutive text from `begin` that is also an entity?
    """
    low = begin
    high = len(sentence)
    best_high = -1
    best_text = None
    while high >= low: 
        mid = (high + low) // 2
        test_text = wikidata_adapter_v2.WikidataAdapter_V2(_join_text_flair(sentence[begin:mid]))
        if test_text:
            best_high = mid
            best_text = test_text
            low = mid + 1
        else:
            high = mid - 1
    return best_high - 1, test_text  # best_high - 1 because mid is used as end of a slice, rather than an index


def disambiguate_v2(query) -> List[Entity]:
    sentence = Sentence(query)
    tagger.predict(sentence)
    embeded_sentence = False
    logging.log(logging.DEBUG, sentence)
    most_likely_entities = []
    trailing = 0
    token_index = 0
    while token_index < len(sentence):
        token = sentence[token_index]
        if token.get_tag('pos').value in [NOUN_TAG, PROPN_TAG]:
            next_index, entity = _longest_entity(sentence, token_index)
            if entity:
                # found an entity!!!
                # embed the sentences in two ways, forward and backward
                if not embeded_sentence:
                    embeddings.embed(sentence)
                    embeded_sentence = True
                # now what are the trailing tokens?
                # the var `trailing` is from previous entity!
                preceding_part = []
                if trailing < token_index:
                    preceding_part = sentence[trailing:token_index]
                # now update `trailing`
                for trailing in range(next_index + 1, len(sentence)):
                    if sentence[trailing].get_tag('pos').value in [ADJ_TAG, VERB_TAG]:
                        break
                succeeding_part = []
                if next_index < trailing:
                    succeeding_part = sentence[next_index+1:trailing+1]
                # get possible entities
                similarities = []
                if preceding_part or succeeding_part:
                    # reduce two arrays of embedding to a number of maximum similarity
                    _, possible_entities = entity.to_entity_list()
                    for possible_entity in possible_entities:
                        desc = Sentence(possible_entity.description)
                        embeddings.embed(desc)
                        best_sim = sentence_similarity(desc, preceding_part + succeeding_part)
                        similarities.append(best_sim)
                    most_likely_index = np.argmax(similarities)   # bayes rule seems does not work
                else:
                    most_likely_index = np.argmax([entity.probability for entity in possible_entities])
                possible_entities[most_likely_index].start_pos = sentence[token_index].start_pos
                possible_entities[most_likely_index].end_pos = sentence[next_index].end_pos
                most_likely_entities.append(possible_entities[most_likely_index])
                token_index = trailing + 1
        else:
            token_index += 1
    logging.log(logging.DEBUG, most_likely_entities)
    return most_likely_entities if most_likely_entities else None
      
