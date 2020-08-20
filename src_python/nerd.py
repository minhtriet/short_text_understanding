"""
I implement this as a module instead of a class as it is intended to be a singleton
https://stackoverflow.com/a/6760726
"""

import wikidata_adapter
import wikidata_adapter_v2
import math
from base_adapter import Entity
from flair.models import SequenceTagger
from flair.data import Sentence, Token
from typing import List
from flair.embeddings import FlairEmbeddings, PooledFlairEmbeddings, StackedEmbeddings
from scipy import special
import numpy as np
from flair.embeddings import WordEmbeddings
import sys
import logging

NOUN_TAG = 'NOUN'
PROPN_TAG = 'PROPN'
VERB_TAG = 'VERB'
ADJ_TAG = 'ADJ'

tagger = SequenceTagger.load('upos-fast')
glove_embedding = WordEmbeddings('glove')
flair_embedding_forward = FlairEmbeddings('news-forward')
flair_embedding_backward = FlairEmbeddings('news-backward')
embedding_types = [
    PooledFlairEmbeddings('news-forward', pooling='min'),
    PooledFlairEmbeddings('news-backward', pooling='min'),
]
embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)


logger = logging.getLogger('app')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

eng_stopwords = ["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above",
                 "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj",
                 "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah",
                 "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also",
                 "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another",
                 "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap",
                 "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent",
                 "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av",
                 "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd",
                 "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin",
                 "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best",
                 "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br",
                 "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came",
                 "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg",
                 "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes",
                 "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains",
                 "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs",
                 "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de",
                 "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't",
                 "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down",
                 "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each",
                 "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven",
                 "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er",
                 "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever",  "everyone", "everything",
                 "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa",
                 "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first",
                 "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty",
                 "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz",]
# nltk don't cut it


def sentence_similarity(sent_1, sent_2) -> float:
    filtered_1 = [t for t in sent_1 if t.text not in eng_stopwords]
    filtered_2 = [t for t in sent_2 if t.text not in eng_stopwords]
    if len(filtered_1) == 0 or len(filtered_2) == 0:
        return 0
    # the below is for debug info
#    print(["...".join([token_prime.text, token.text])
#           for token in filtered_1 for token_prime in filtered_2])
#    print([np.dot(token_prime.embedding, token.embedding) for token in filtered_1 for token_prime in filtered_2])
    return max([np.dot(token_prime.embedding, token.embedding)
                for token in filtered_1 for token_prime in filtered_2])


def disambiguate(query) -> List[Entity]:
    sentence = Sentence(query)
    tagger.predict(sentence)
    logging.log(logging.DEBUG, sentence)
    most_likely_entities = []
    trailing = 0
    token_index = 0
    while token_index < len(sentence.tokens):
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
                        desc_1 = Sentence(entity.description)
                        flair_embedding_backward.embed(desc_1)
                        desc_2 = Sentence(entity.description)
                        flair_embedding_forward.embed(desc_2)
                        best_sim = max(sentence_similarity(desc_1, preceding_part), sentence_similarity(desc_2, succeeding_part))
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
        mid = int(math.ceil((high + low)*0.5))
        test_text = wikidata_adapter_v2.WikidataAdapter_V2(_join_text_flair(sentence[begin:mid]))
        if test_text:
            best_high = mid
            best_text = test_text
            low = mid + 1
        else:
            high = mid - 1
    return best_high - 1, best_text  # best_high - 1 because mid is used as end of a slice, rather than an index


def disambiguate_v2(query) -> List[Entity]:
    sentence = Sentence(query)
    tagger.predict(sentence)
    logging.log(logging.DEBUG, sentence)
    most_likely_entities = []
    trailing = 0  # the part that is after an entity but contribute to the understanding of the entity
    token_index = 0
    while token_index < len(sentence):
        token = sentence[token_index]
        if token.get_tag('pos').value == VERB_TAG:
            token_index += 1
            continue
        next_index, entity = _longest_entity(sentence, token_index)
        if entity:
            # found an entity!!!
            preceding_part = []
            if trailing < token_index:
                preceding_part = Sentence(_join_text_flair(sentence[trailing:token_index]))
                flair_embedding_forward.embed(preceding_part)
            # now update `trailing`
            succeeding_part = []
            trailing = next_index + 1
            while trailing < len(sentence):  # use while loop to solve the case when noun is at the end of the query
                if sentence[trailing].get_tag('pos').value in [ADJ_TAG, VERB_TAG] or sentence[trailing].text in eng_stopwords:
                    break
                trailing += 1
            if next_index < trailing:
                succeeding_part = Sentence(_join_text_flair(sentence[next_index+1:trailing]))
                flair_embedding_backward.embed(succeeding_part)
            # get possible entities
            similarities = []
            _, possible_entities = entity.to_entity_list()
            if possible_entities:
                if preceding_part or succeeding_part:
                    # reduce two arrays of embedding to a number of maximum similarity
                    for possible_entity in possible_entities:
                        desc = Sentence(possible_entity.description)
                        flair_embedding_forward.embed(desc)
                        back_desc = Sentence(possible_entity.description)
                        flair_embedding_backward.embed(back_desc)
                        best_sim = max([sentence_similarity(desc[:4], preceding_part), sentence_similarity(back_desc[:4], succeeding_part)])
                        similarities.append(best_sim)
                    most_likely_index = np.argmax(similarities)   # bayes rule seems does not work
                else:
                    most_likely_index = np.argmax([entity.probability for entity in possible_entities])
                possible_entities[most_likely_index].start_pos = sentence[token_index].start_pos
                possible_entities[most_likely_index].end_pos = sentence[next_index].end_pos
                most_likely_entities.append(possible_entities[most_likely_index])
            token_index = max(trailing, next_index) + 1
        else:
            token_index += 1
    logging.log(logging.DEBUG, most_likely_entities)
    return most_likely_entities if most_likely_entities else None
