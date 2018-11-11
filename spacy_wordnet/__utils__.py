import glob
import os
from collections import defaultdict
from typing import Optional, List, Dict, Set

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


def spacy2wordnet_pos(spacy_pos: int) -> Optional[str]:
    return __WN_POS_MAPPING.get(spacy_pos)


def fetch_wordnet_lang(lang: Optional[str] = None) -> str:
    language = __WN_LANGUAGES_MAPPING.get(lang, None)

    if not language:
        raise Exception('Language {} not supported'.format(lang))

    return language


def _persist_wordnet_domains(path: str, domains: Dict[str, Set[str]]):
    with open(path, 'w') as file:
        file.writelines(['{}\n'.format('\t'.join([k, ' '.join(v)])) for k, v in domains.items()])
        file.close()


def _load_wordnet_domains_from_ppv(path: str, threshold: float = 0.00009) -> Dict[str, List[str]]:
    def domain_name_from_filename(filename: str) -> str:
        name, _ = os.path.splitext(os.path.basename(filename))
        return name

    domains_by_ssid = defaultdict(list)

    for filename in glob.glob(path):
        domain_name = domain_name_from_filename(filename)
        for line in open(filename, 'r'):
            ssid, weight = line.strip().split('\t')
            if float(weight) >= threshold:
                domains_by_ssid[ssid].append(domain_name)

    return domains_by_ssid


def _load_wordnet_domains_from_txt(filepath: str) -> Dict[str, List[str]]:
    domains_by_ssid = defaultdict(list)
    for filename in glob.glob(filepath):
        for line in open(filename, 'r'):
            row = line.strip().split(' ')
            ssid = row[0]
            domains = row[2:]
            domains_by_ssid[ssid].extend(domains)

    return domains_by_ssid
