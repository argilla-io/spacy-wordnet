# spaCy WordNet

spaCy Wordnet is a simple custom component for using [WordNet](https://wordnet.princeton.edu/), [MultiWordnet](http://multiwordnet.fbk.eu/english/home.php) and [WordNet domains](http://wndomains.fbk.eu/) with [spaCy](http://spacy.io).

The component combines the [NLTK wordnet interface](http://www.nltk.org/howto/wordnet.html) with WordNet domains to allow users to:

* Get all synsets for a processed token. For example, getting all the synsets (word senses) of the word ``bank``.
* Get and filter synsets by domain. For example, getting synonyms of the verb ``withdraw`` in the financial domain.

 
## Getting started
The spaCy WordNet component can be easily integrated into spaCy pipelines. You just need the following:
### Prerequisites

* Python 3.X
* spaCy 2.X

You also need to install the following NLTK wordnet data:

````bash
python -m nltk.downloader wordnet
python -m nltk.downloader omw
````
### Install

````bash
pip install spacy-wordnet
````


### Supported languages
Almost all Open Multi Wordnet languages are supported.

## Usage


### English example

````python

import spacy

from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

# Load a spacy model (almost all Open Multi Wordnet languages are supported)
nlp = spacy.load('en')

# with spacy 2
nlp.add_pipe(WordnetAnnotator(nlp, 'wordnet'), after='tagger')
# with spacy 3
nlp.add_pipe('wordnet')
token = nlp('prices')[0]

# wordnet object link spacy token with nltk wordnet interface by giving acces to
# synsets and lemmas 
token._.wordnet.synsets()
token._.wordnet.lemmas()

# And automatically tags with wordnet domains
token._.wordnet.wordnet_domains()
````

spaCy WordNet lets you find synonyms by domain of interest for example economy
````python
economy_domains = ['finance', 'banking']
enriched_sentence = []
sentence = nlp('I want to withdraw 5,000 euros')

# For each token in the sentence
for token in sentence:
    # We get those synsets within the desired domains
    synsets = token._.wordnet.wordnet_synsets_for_domain(economy_domains)
    if not synsets:
        enriched_sentence.append(token.text)
    else:
	lang = token._.wordnet.lang()
        lemmas_for_synset = [lemma for s in synsets for lemma in s.lemma_names(lang)]
        # If we found a synset in the economy domains
        # we get the variants and add them to the enriched sentence
        enriched_sentence.append('({})'.format('|'.join(set(lemmas_for_synset))))

# Let's see our enriched sentence
print(' '.join(enriched_sentence))
# >> I (need|want|require) to (draw|withdraw|draw_off|take_out) 5,000 euros
    
````

### Portuguese example

```python
import spacy

from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

# Load an spacy model (you need to download the spacy pt model) 
nlp = spacy.load('pt')
nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')
text = "Eu quero retirar 5.000 euros"
economy_domains = ['finance', 'banking']
enriched_sentence = []
sentence = nlp(text)

# For each token in the sentence
for token in sentence:
    # We get those synsets within the desired domains
    synsets = token._.wordnet.wordnet_synsets_for_domain(economy_domains)
    if not synsets:
        enriched_sentence.append(token.text)
    else:
	lang = token._.wordnet.lang()
        lemmas_for_synset = [lemma for s in synsets for lemma in s.lemma_names(lang)]
        # If we found a synset in the economy domains
        # we get the variants and add them to the enriched sentence
        enriched_sentence.append('({})'.format('|'.join(set(lemmas_for_synset))))

# Let's see our enriched sentence
print(' '.join(enriched_sentence))
# >> Eu (querer|desejar|esperar) retirar 5.000 euros
```


