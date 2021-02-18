
from spacy.tokens.doc       import Doc
from spacy.tokens.token     import Token
from spacy.parts_of_speech  import *
from spacy.language         import Language

from spacy_wordnet.wordnet_domains import Wordnet, load_wordnet_domains

class WordnetAnnotator:
    __FIELD = 'wordnet'

    def __init__(self, nlp, name):
        self.__lang = nlp.lang
        Token.set_extension(WordnetAnnotator.__FIELD, default=None, force=True)
        load_wordnet_domains()

    def __call__(self, doc: Doc):
        for token in doc:
            wordnet = Wordnet(token=token, lang=self.__lang)
            token._.set(WordnetAnnotator.__FIELD, wordnet)

        return doc

#TODO: handle also spacy2
try:
    @Language.factory("wordnet")
    def make_WA(nlp, name):
        return WordnetAnnotator(nlp, name)
except:
    pass
