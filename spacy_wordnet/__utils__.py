import glob
import os
from collections import defaultdict
from typing import Optional, List

from nltk.corpus.reader.wordnet import \
    ADJ as WN_ADJ, \
    ADV as WN_ADV, \
    NOUN as WN_NOUN, \
    VERB as WN_VERB, Synset

from spacy.parts_of_speech import ADJ, ADV, NOUN, VERB, AUX

from spacy_wordnet import get_package_basepath

__DEFAULT_LANG = 'spa'
__WN_LANGUAGES_MAPPING = dict(es=__DEFAULT_LANG, en='eng')
__WN_POS_MAPPING = {
    ADJ: WN_ADJ,
    NOUN: WN_NOUN,
    ADV: WN_ADV,
    VERB: WN_VERB,
    AUX: WN_VERB
}

__WN_DOMAINS_PATH = os.path.join(get_package_basepath(), 'data/wordnet_domains/*.ppv')

__WN_DOMAINS_BY_SSID = defaultdict(list)


def wordnet_domains_path() -> str:
    return __WN_DOMAINS_PATH


def load_wordnet_domains(path: str, threshold: float = 0.0009):
    def domain_name_from_filename(filename: str) -> str:
        name, _ = os.path.splitext(os.path.basename(filename))
        return name

    if __WN_DOMAINS_BY_SSID:
        return

    for filename in glob.glob(path):
        domain_name = domain_name_from_filename(filename)
        for line in open(filename, 'r'):
            ssid, weight = line.strip().split('\t')
            if float(weight) >= threshold:
                __WN_DOMAINS_BY_SSID[ssid].append(domain_name)


def get_domains_for_synset(synset: Synset) -> List[str]:
    ssid = '{}-{}'.format(str(synset.offset()).zfill(8), synset.pos())
    return __WN_DOMAINS_BY_SSID.get(ssid, [])


def spacy2wordnet_pos(spacy_pos: int) -> Optional[str]:
    return __WN_POS_MAPPING.get(spacy_pos)


def fetch_wordnet_lang(lang: Optional[str] = None) -> str:
    language = __WN_LANGUAGES_MAPPING.get(lang, None)

    if not language:
        raise Exception('Language {} not supported'.format(lang))

    return language
