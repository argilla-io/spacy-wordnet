import os
import spacy_wordnet

__PACKAGE_BASE_PATH = os.path.dirname(spacy_wordnet.__file__)


def get_package_basepath():
    return __PACKAGE_BASE_PATH
