# spaCy WordNet

spaCy Wordnet is a simple custom component for using [WordNet](https://wordnet.princeton.edu/), [MultiWordnet](http://multiwordnet.fbk.eu/english/home.php) and [WordNet domains](http://wndomains.fbk.eu/) with [spaCy](http://spacy.io).

The component combines the [NLTK wordnet interface](http://www.nltk.org/howto/wordnet.html) with WordNet domains to allow users to:

* Get all synsets for a processed token. For example, getting all the synsets (word senses) of the word ``bank``.
* Get and filter synsets by domain. For example, getting synonyms of the verb ``withdraw`` in the financial domain.

 
## Getting started
The spaCy WordNet component can be easily integrated into spaCy pipelines. You just need the following:
### Prerequisites

* Python 3.X
* spaCy

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

Once you choose the desired language (from the list of supported ones above), you will need to manually download a spaCy model for it. Check the list of available models for each language at [SpaCy 2.x](https://v2.spacy.io/models) or [SpaCy 3.x](https://spacy.io/usage/models).

### English example

Download example model:
```bash
python -m spacy download en_core_web_sm
```

Run:
````python

import spacy

from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

# Load an spacy model
nlp = spacy.load('en_core_web_sm')
# Spacy 3.x
nlp.add_pipe("spacy_wordnet", after='tagger')
# Spacy 2.x
# nlp.add_pipe(WordnetAnnotator(nlp, name="spacy_wordnet"), after='tagger')
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
        lemmas_for_synset = [lemma for s in synsets for lemma in s.lemma_names()]
        # If we found a synset in the economy domains
        # we get the variants and add them to the enriched sentence
        enriched_sentence.append('({})'.format('|'.join(set(lemmas_for_synset))))

# Let's see our enriched sentence
print(' '.join(enriched_sentence))
# >> I (need|want|require) to (draw|withdraw|draw_off|take_out) 5,000 euros
    
````

### Portuguese example

Download example model:
```bash
python -m spacy download pt_core_news_sm
```

Run:
```python
import spacy

from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

# Load an spacy model
nlp = spacy.load('pt_core_news_sm')
# Spacy 3.x
nlp.add_pipe("spacy_wordnet", after='tagger', config={'lang': nlp.lang})
# Spacy 2.x
# nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')
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
        lemmas_for_synset = [lemma for s in synsets for lemma in s.lemma_names('por')]
        # If we found a synset in the economy domains
        # we get the variants and add them to the enriched sentence
        enriched_sentence.append('({})'.format('|'.join(set(lemmas_for_synset))))

# Let's see our enriched sentence
print(' '.join(enriched_sentence))
# >> Eu (querer|desejar|esperar) retirar 5.000 euros
```
