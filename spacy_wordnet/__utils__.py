import glob
import os
from collections import defaultdict
from typing import Optional, List, Dict, Set

from nltk.corpus.reader.wordnet import (
    ADJ as WN_ADJ,
    ADV as WN_ADV,
    NOUN as WN_NOUN,
    VERB as WN_VERB,
    Synset,
)

from spacy.parts_of_speech import ADJ, ADV, NOUN, VERB, AUX

from spacy_wordnet import get_package_basepath

# The Open Multi Wordnet corpus contains the following languages:
#   als arb bul cat cmn dan ell eus fas fin fra glg heb hrv ind ita jpn nld nno nob pol por qcn slv spa swe tha zsm
#   ('deu' can be found in Extended Open Multi Wordnet)
# the available spacy languages are:
# af am ar bg bn ca cs da de el en es et eu fa fi fr ga gu he hi hr hu hy id is it ja kn ko ky lb lij
# lt lv mk ml mr nb ne nl pl pt ro ru sa si sk sl sq sr sv ta te th ti tl tn tr tt uk ur vi xx yo zh
# then the full mapping is
__DEFAULT_LANG = "spa"
__WN_LANGUAGES_MAPPING = dict(
    es=__DEFAULT_LANG,
    en="eng",
    fr="fra",
    it="ita",
    pt="por",
    de="deu",
    # other languages from omw
    sq="als",  # Albanian
    ar="arb",  # Arabic
    bg="bul",  # Bulgarian
    ca="cat",  # Catalan
    zh="cmn",  # Chinese Open Wordnet
    da="dan",  # Danish
    el="ell",  # Greek
    eu="eus",  # Basque
    fa="fas",  # Persian
    fi="fin",  # Finnish
    # ?? ='glg',  # Galician
    he="heb",  # Hebrew
    hr="hrv",  # Croatian
    id="ind",  # Indonesian
    ja="jpn",  # Japanese
    nl="nld",  # Dutch
    # no ='nno', # Norwegian
    # nb ='nob', # Norwegian Bokmal
    pl="pol",  # Polish
    # ?? ='qcn', # Chinese (Taiwan)
    sl="slv",  # Slovenian
    sv="swe",  # Swedish
    th="tha",  # Thai
    ml="zsm",  # Malayalam
)
__WN_POS_MAPPING = {
    ADJ: WN_ADJ,
    NOUN: WN_NOUN,
    ADV: WN_ADV,
    VERB: WN_VERB,
    AUX: WN_VERB,
}


def spacy2wordnet_pos(spacy_pos: int) -> Optional[str]:
    return __WN_POS_MAPPING.get(spacy_pos)


def fetch_wordnet_lang(lang: Optional[str] = None) -> str:
    language = __WN_LANGUAGES_MAPPING.get(lang, None)

    if not language:
        raise Exception("Language {} not supported".format(lang))

    return language


def _persist_wordnet_domains(path: str, domains: Dict[str, Set[str]]):
    with open(path, "w") as file:
        file.writelines(
            ["{}\n".format("\t".join([k, " ".join(v)])) for k, v in domains.items()]
        )
        file.close()


def _load_wordnet_domains_from_ppv(
    path: str, threshold: float = 0.00009
) -> Dict[str, List[str]]:
    def domain_name_from_filename(filename: str) -> str:
        name, _ = os.path.splitext(os.path.basename(filename))
        return name

    domains_by_ssid = defaultdict(list)

    for filename in glob.glob(path):
        domain_name = domain_name_from_filename(filename)
        for line in open(filename, "r"):
            ssid, weight = line.strip().split("\t")
            if float(weight) >= threshold:
                domains_by_ssid[ssid].append(domain_name)

    return domains_by_ssid


def _load_wordnet_domains_from_txt(filepath: str) -> Dict[str, List[str]]:
    domains_by_ssid = defaultdict(list)
    for filename in glob.glob(filepath):
        for line in open(filename, "r"):
            row = line.strip().split(" ")
            ssid = row[0]
            domains = row[2:]
            domains_by_ssid[ssid].extend(domains)

    return domains_by_ssid
