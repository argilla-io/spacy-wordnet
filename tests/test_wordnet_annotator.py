import unittest
from collections import defaultdict

import spacy

import numpy as np

from itertools import product

from spacy_wordnet.wordnet_annotator import WordnetAnnotator


class WordnetAnnotatorTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.nlp_en = spacy.load('en')
        self.nlp_es = spacy.load('es')

        # Add wordnet component
        self.nlp_en.add_pipe(WordnetAnnotator(self.nlp_en.lang))
        self.nlp_es.add_pipe(WordnetAnnotator(self.nlp_es.lang))

    def test_english_annotations(self):

        token = self.nlp_en('contracts')[0]

        assert token._.wordnet.synsets()
        assert token._.wordnet.lemmas()
        assert token._.wordnet.wordnet_domains()

    def test_generate_variants_from_domain_list(self):

        economy_domains = ['finance', 'banking']
        enriched_sentence = []

        sentence = self.nlp_en('I want to withdraw 5,000 euros')

        for token in sentence:
            synsets = token._.wordnet.wordnet_synsets_for_domain(economy_domains)

            if synsets:
                lemmas_for_synset = []
                for s in synsets:
                    lemmas_for_synset.extend(s.lemma_names())
                enriched_sentence.append('({})'.format('|'.join(set(lemmas_for_synset))))
            else:
                enriched_sentence.append(token.text)
        print(' '.join(enriched_sentence))

    def test_spanish_annotations(self):
        token = self.nlp_es('contratos')[0]

        assert token._.wordnet.synsets()
        assert token._.wordnet.lemmas()
        assert token._.wordnet.wordnet_domains()
