# Spacy wordnet annotator

`spacy-wordnet` creates annotations that easily allow the use of wordnet 
and [wordnet domains](http://wndomains.fbk.eu/) by using 
the [nltk wordnet interface](http://www.nltk.org/howto/wordnet.html)
 



## Install

````bash
pip install spacy-wordnet
````

## Requirements
Some nltk data must be installed before using this package

````bash
python -m nltk.downloader wordnet
python -m nltk.downloader omw

````

## Usage

````python

import spacy

from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

# Load an spacy model (supported models are "es" and "en") 
nlp = spacy.load('en')
nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')
token = nlp('prices')[0]

# wordnet object link spacy token with nltk wordnet interface by giving acces to
# synsets and lemmas 
token._.wordnet.synsets()
token._.wordnet.lemmas()

# And automatically tags with wordnet domains
token._.wordnet.wordnet_domains()
    
````

