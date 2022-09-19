import unittest

from nltk.corpus import wordnet as wn
import spacy

from spacy_wordnet.wordnet_annotator import WordnetAnnotator


class WordnetAnnotatorTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_es = spacy.load("es_core_news_sm")

        try:
            # Add wordnet component
            self.nlp_en.add_pipe("spacy_wordnet")
            self.nlp_es.add_pipe("spacy_wordnet")
        except (ValueError, TypeError):  # spacy 2.x
            self.nlp_en.add_pipe(WordnetAnnotator(self.nlp_en, name="spacy_wordnet"))
            self.nlp_es.add_pipe(WordnetAnnotator(self.nlp_es, name="spacy_wordnet"))

    def test_english_annotations(self):

        token = self.nlp_en("contracts")[0]

        assert token._.wordnet.synsets()
        assert token._.wordnet.lemmas()
        assert token._.wordnet.wordnet_domains()

        actual_none_synsets = set(token._.wordnet.synsets(pos=None))
        expected_none_synsets = {wn.synset("contract.n.01"),
                                 wn.synset("contract.n.02"),
                                 wn.synset("contract.n.03")}
        assert actual_none_synsets == expected_none_synsets

        actual_verb_synsets = set(token._.wordnet.synsets(pos="verb"))
        expected_verb_synsets = {wn.synset('abridge.v.01'),
                                 wn.synset('compress.v.02'),
                                 wn.synset('condense.v.07'),
                                 wn.synset('contract.v.01'),
                                 wn.synset('contract.v.04'),
                                 wn.synset('contract.v.06'),
                                 wn.synset('narrow.v.01'),
                                 wn.synset('shrink.v.04'),
                                 wn.synset('sign.v.04')}
        assert actual_verb_synsets == expected_verb_synsets

        actual_noun_synsets = set(token._.wordnet.synsets(pos="noun"))
        expected_noun_synsets = {wn.synset('contract.n.01'),
                                 wn.synset('contract.n.02'),
                                 wn.synset('contract.n.03')}
        assert actual_noun_synsets == expected_noun_synsets

        actual_adj_synsets = set(token._.wordnet.synsets(pos="adj"))
        expected_adj_synsets = set()
        assert actual_adj_synsets == expected_adj_synsets

        actual_verb_noun_synsets = set(token._.wordnet.synsets(
            pos=["verb", "noun"])
        )
        expected_verb_noun_synsets = {wn.synset('abridge.v.01'),
                                      wn.synset('compress.v.02'),
                                      wn.synset('condense.v.07'),
                                      wn.synset('contract.v.01'),
                                      wn.synset('contract.v.04'),
                                      wn.synset('contract.v.06'),
                                      wn.synset('narrow.v.01'),
                                      wn.synset('shrink.v.04'),
                                      wn.synset('sign.v.04'),
                                      wn.synset('contract.n.01'),
                                      wn.synset('contract.n.02'),
                                      wn.synset('contract.n.03')}
        assert actual_verb_noun_synsets == expected_verb_noun_synsets

    def test_generate_variants_from_domain_list(self):

        economy_domains = ["finance", "banking"]
        enriched_sentence = []

        sentence = self.nlp_en("I want to withdraw 5,000 euros")

        for token in sentence:
            synsets = token._.wordnet.wordnet_synsets_for_domain(economy_domains)

            if synsets:
                lemmas_for_synset = []
                for s in synsets:
                    lemmas_for_synset.extend(s.lemma_names())
                enriched_sentence.append(
                    "({})".format("|".join(set(lemmas_for_synset)))
                )
            else:
                enriched_sentence.append(token.text)
        print(" ".join(enriched_sentence))

    def test_spanish_annotations(self):
        token = self.nlp_es("contratos")[0]

        assert token._.wordnet.synsets()
        assert token._.wordnet.lemmas()
        assert token._.wordnet.wordnet_domains()
