from collections import defaultdict
from itertools import chain

from spacy_wordnet.__utils__ import _load_wordnet_domains_from_ppv, _load_wordnet_domains_from_txt, \
    _persist_wordnet_domains

ppv_path = 'wordnet_domains/*.ppv'
txt_path = 'wordnet_domains/*.txt'


def run():
    domains_ppv = _load_wordnet_domains_from_ppv(ppv_path)
    domains_txt = _load_wordnet_domains_from_txt(txt_path)
    domains = defaultdict(set)
    for k, v in chain(domains_ppv.items(), domains_txt.items()):
        for domain in v:
            domains[k].add(domain)

    _persist_wordnet_domains('wordnet_domains.txt', domains)


if __name__ == '__main__':
    run()
