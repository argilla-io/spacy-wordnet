from spacy.tokens.doc import Doc
from spacy.tokens.token import Token
from spacy.language import Language

from spacy_wordnet.wordnet_domains import Wordnet, load_wordnet_domains


@Language.factory("wordnet")
class WordnetAnnotator(object):
    __FIELD = 'wordnet'

    def __init__(self, nlp, name):
        Token.set_extension(WordnetAnnotator.__FIELD, default=None, force=True)
        load_wordnet_domains()
        self.__lang = nlp.lang

    def __call__(self, doc: Doc):
        for token in doc:
            wordnet = Wordnet(token=token, lang=self.__lang)
            token._.set(WordnetAnnotator.__FIELD, wordnet)

        return doc
