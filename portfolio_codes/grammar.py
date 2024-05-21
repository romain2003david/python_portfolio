import nltk
#nltk.download()
from nltk.corpus import treebank
import os

print(os.getcwd())
# Load the Penn Treebank corpus
corpus = treebank.tagged_sents()

# Train a Hidden Markov Model (HMM) tagger
hmm_tagger = nltk.tag.HiddenMarkovModelTagger.train(corpus)

# Extract transition probabilities from the HMM tagger
transition_probabilities = hmm_tagger._transitions
#print(transition_probabilities['NN'].prob('VB'))
w_types = list(transition_probabilities.keys())

#pos_tags = nltk.help.upenn_tagset()

# Print transition probabilities for demonstration
"""
with open("README_grammar_markov_english_model.txt", "w") as file:
    
    for i in w_types:
"""

with open("grammar_markov_english_model.txt", "w") as file:
    
    for i in w_types:
        for j in w_types:
            prob = transition_probabilities[i].prob(j)
            #print(i, j, prob)
            file.write(str(prob)+" ")
        file.write("\n")