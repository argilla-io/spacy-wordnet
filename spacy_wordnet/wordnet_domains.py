from typing import Union
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
from spacy.tokens.token import Token

from spacy_wordnet.__utils__ import *

__WN_DOMAINS_PATH = os.path.join(get_package_basepath(), "data/wordnet_domains.txt")

__WN_DOMAINS_BY_SSID = defaultdict(list)


def wordnet_domains_path() -> str:
    return __WN_DOMAINS_PATH


def load_wordnet_domains(path: Optional[str] = wordnet_domains_path()):
    if __WN_DOMAINS_BY_SSID:
        return

    for line in open(path, "r"):
        ssid, domains = line.strip().split("\t")
        __WN_DOMAINS_BY_SSID[ssid] = domains.split(" ")


def get_domains_for_synset(synset: Synset) -> List[str]:
    ssid = "{}-{}".format(str(synset.offset()).zfill(8), synset.pos())
    return __WN_DOMAINS_BY_SSID.get(ssid, [])


class Wordnet(object):

    # # TODO: add serialization
    # def to_disk(self, path):
    #     # save:
    #     # __token?
    #     # __lang?
    #     # __synsets
    #     # __lemmas
    #     # __wordnet_domains
    #     pass
    # def from_disk(self, path):
    #     pass

    def __init__(self, token: Token, lang: str = "es"):
        self.__token = token
        self.__lang = fetch_wordnet_lang(lang)
        self.__synsets = self.__find_synsets
        self.__lemmas = self.__find_lemmas()
        self.__wordnet_domains = self.__find_wordnet_domains()

    def synsets(self, pos: Optional[Union[str, List[str]]] = None) -> List[Synset]:
        """
        Load all synsets with a given part of speech tag.
        If no pos is specified and `token.pos` is a VERB, NOUN, 
        or ADJ, synsets with the same parts of speech as 
        `token.pos` will be loaded. If `token.pos` is not a 
        VERB, NOUN, or ADJ and no pos is specified, an empty 
        list will be returned.

        :param pos: filter returned synsets by part(s) of speech.
            Acceptable values are "verb", "noun", and "adj".
        :return: list of synsets
        """
        return self.__synsets(self.__token, self.__lang, pos=pos)

    def lang(self):
        return self.__lang

    def lemmas(self):
        return self.__lemmas

    def wordnet_domains(self):
        return self.__wordnet_domains

    def wordnet_domains_for_synset(self, synset: Synset):
        return get_domains_for_synset(synset)

    def wordnet_synsets_for_domain(self, domains: List[str]):
        return [
            synset for synset in self.synsets() if self.__has_domains(synset, domains)
        ]

    @staticmethod
    def __find_synsets(token: Token,
                       lang: str,
                       pos: Optional[Union[str, List[str]]] = None) -> List[Synset]:
        if pos is None:
            pos = []
        elif isinstance(pos, str):
            pos = [pos]
        elif not isinstance(pos, list):
            try:
                pos = list(pos)
            except TypeError:
                raise TypeError("pos argument must be None, type str, or type list.")
        
        acceptable_pos = {"verb": VERB, "noun": NOUN, "adj": ADJ} # We can define this as a private class constant
        # check if any element in `pos` is not in `acceptable_pos`
        if set(pos).difference(acceptable_pos):
            raise ValueError("pos argument must be a combination of 'verb', "
                             "'noun', or 'adj'.")

        token_pos: List[int] = [acceptable_pos[k] for k in pos]
        if not token_pos:
           token_pos = [token.pos]
        word_variants = [token.text]
        if token.pos in (token_pos if pos else acceptable_pos.values()):
            # extend synset coverage using lemmas
            word_variants.append(token.lemma_)

        for word in word_variants:
            token_synsets: List[Synset] = []
            for p in token_pos:
                token_synsets.extend(wn.synsets(
                    word, pos=spacy2wordnet_pos(p), lang=lang
                ))

            if token_synsets:
                return token_synsets

        return []

    @staticmethod
    def __has_domains(synset: Synset, domains: List[str]) -> bool:
        return not set(domains).isdisjoint(get_domains_for_synset(synset))

    def __find_wordnet_domains(self):
        return [
            domain
            for synset in self.synsets()
            for domain in get_domains_for_synset(synset)
        ]

    def __find_lemmas(self):
        return [lemma for synset in self.synsets() for lemma in synset.lemmas(lang=self.__lang)]
