from spacy.tokens.doc import Doc
from spacy.tokens.token import Token
from spacy.language import Language

from spacy_wordnet.wordnet_domains import Wordnet, load_wordnet_domains

try:

    @Language.factory("spacy_wordnet", default_config={"lang": "en"})
    def wordnet_annotator(nlp, name, lang: str):
        return WordnetAnnotator(lang=lang)


except AttributeError:
    pass  # spacy 2.x


class WordnetAnnotator(object):
    __FIELD = "wordnet"

    def __init__(self, lang: str = "es"):
        Token.set_extension(WordnetAnnotator.__FIELD, default=None, force=True)
        load_wordnet_domains()
        self.__lang = lang

    def __call__(self, doc: Doc):
        for token in doc:
            wordnet = Wordnet(token=token, lang=self.__lang)
            token._.set(WordnetAnnotator.__FIELD, wordnet)

        return doc
