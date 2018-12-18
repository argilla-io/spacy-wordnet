import spacy

from spacy_wordnet.wordnet_annotator import WordnetAnnotator

if __name__ == '__main__':
    import nltk
    nltk.download('wordnet')

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

    # Imagine we want to enrich the following sentence with synonyms
    sentence = nlp('I want to withdraw 5,000 euros')

    # spaCy WordNet lets you find synonyms by domain of interest
    # for example economy
    economy_domains = ['finance', 'banking']
    enriched_sentence = []

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
