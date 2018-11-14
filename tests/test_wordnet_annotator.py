import unittest

import spacy

from spacy_wordnet.wordnet_annotator import WordnetAnnotator


class WordnetAnnotatorTest(unittest.TestCase):

    def test_english_annotations(self):
        nlp = spacy.load('en')
        nlp.add_pipe(WordnetAnnotator(nlp.lang))

        token = nlp('contracts')[0]

        assert token._.wordnet.synsets()
        assert token._.wordnet.lemmas()
        assert token._.wordnet.wordnet_domains()

        del nlp

    def test_spanish_annotations(self):
        nlp = spacy.load('es')
        nlp.add_pipe(WordnetAnnotator(nlp.lang))

        token = nlp('contratos')[0]

        assert token._.wordnet.synsets()
        assert token._.wordnet.lemmas()
        assert token._.wordnet.wordnet_domains()

        del nlp
